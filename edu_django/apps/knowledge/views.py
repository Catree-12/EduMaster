from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count

from .models import Tag, TagRelation, KnowledgePoint, KnowledgePointRelation


# ==================== 标签管理 ====================
class TagManageView(APIView):
    """
    GET  /api/knowledge/tags/ - 获取标签列表
    POST /api/knowledge/tags/ - 创建标签
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """获取标签列表（支持搜索和分页）"""
        course_id = request.query_params.get('course_id')
        keyword = request.query_params.get('keyword', '')
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('pageSize', 20))
        
        queryset = Tag.objects.all()
        
        # 按课程过滤
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        
        if keyword:
            queryset = queryset.filter(name__icontains=keyword)
        
        # 统计每个标签的使用次数
        queryset = queryset.annotate(
            usage_count=Count('tag_rels')
        ).order_by('-usage_count', 'name')
        
        total = queryset.count()
        start = (page - 1) * page_size
        end = start + page_size
        tags = queryset[start:end]
        
        tag_list = [
            {
                'id': tag.id,
                'name': tag.name,
                'usage_count': tag.usage_count,
            }
            for tag in tags
        ]
        
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': {
                'tags': tag_list,
                'total': total,
                'page': page,
                'pageSize': page_size,
            }
        })
    
    def post(self, request):
        """创建新标签"""
        name = request.data.get('name', '').strip()
        course_id = request.data.get('course_id')
        
        if not name:
            return Response({
                'code': 400,
                'message': '标签名称不能为空',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if not course_id:
            return Response({
                'code': 400,
                'message': '课程ID不能为空',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 检查同一课程下标签是否已存在
        if Tag.objects.filter(name=name, course_id=course_id).exists():
            return Response({
                'code': 400,
                'message': '标签已存在',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 验证课程存在
        from courses.models import Course
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({
                'code': 404,
                'message': '课程不存在',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        
        tag = Tag.objects.create(name=name, course=course)
        
        return Response({
            'code': 200,
            'message': '创建成功',
            'data': {
                'id': tag.id,
                'name': tag.name,
            }
        }, status=status.HTTP_201_CREATED)


class TagDetailView(APIView):
    """
    GET    /api/knowledge/tags/{id}/ - 获取标签详情
    PUT    /api/knowledge/tags/{id}/ - 更新标签
    DELETE /api/knowledge/tags/{id}/ - 删除标签
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, tag_id):
        """获取标签详情（包括关联对象列表）"""
        try:
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            return Response({
                'code': 404,
                'message': '标签不存在',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        
        # 获取关联的对象
        relations = TagRelation.objects.filter(tag=tag).select_related('content_type')
        
        related_objects = []
        for rel in relations[:50]:  # 限制返回数量
            related_objects.append({
                'content_type': rel.content_type.model,
                'object_id': rel.object_id,
            })
        
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': {
                'id': tag.id,
                'name': tag.name,
                'usage_count': relations.count(),
                'related_objects': related_objects,
            }
        })
    
    def put(self, request, tag_id):
        """更新标签名称"""
        try:
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            return Response({
                'code': 404,
                'message': '标签不存在',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        
        name = request.data.get('name', '').strip()
        
        if not name:
            return Response({
                'code': 400,
                'message': '标签名称不能为空',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 检查新名称是否与其他标签冲突
        if Tag.objects.filter(name=name).exclude(id=tag_id).exists():
            return Response({
                'code': 400,
                'message': '标签名称已存在',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        tag.name = name
        tag.save()
        
        return Response({
            'code': 200,
            'message': '更新成功',
            'data': {
                'id': tag.id,
                'name': tag.name,
            }
        })
    
    def delete(self, request, tag_id):
        """删除标签（同时删除所有关联）"""
        try:
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            return Response({
                'code': 404,
                'message': '标签不存在',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        
        tag.delete()  # 级联删除所有 TagRelation
        
        return Response({
            'code': 200,
            'message': '删除成功',
            'data': None
        })


class ObjectTagManageView(APIView):
    """
    POST   /api/knowledge/tags/attach/ - 给对象添加标签
    DELETE /api/knowledge/tags/detach/ - 移除对象的标签
    GET    /api/knowledge/tags/object/ - 获取对象的所有标签
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """获取某个对象的所有标签"""
        content_type_name = request.query_params.get('content_type')  # 如 'course', 'lesson'
        object_id = request.query_params.get('object_id')
        
        if not content_type_name or not object_id:
            return Response({
                'code': 400,
                'message': '缺少参数 content_type 或 object_id',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            content_type = ContentType.objects.get(model=content_type_name)
        except ContentType.DoesNotExist:
            return Response({
                'code': 400,
                'message': f'无效的 content_type: {content_type_name}',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        relations = TagRelation.objects.filter(
            content_type=content_type,
            object_id=object_id
        ).select_related('tag')
        
        tags = [
            {
                'id': rel.tag.id,
                'name': rel.tag.name,
            }
            for rel in relations
        ]
        
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': {'tags': tags}
        })
    
    def post(self, request):
        """给对象添加标签"""
        tag_id = request.data.get('tag_id')
        content_type_name = request.data.get('content_type')  # 如 'course', 'lesson'
        object_id = request.data.get('object_id')
        
        if not all([tag_id, content_type_name, object_id]):
            return Response({
                'code': 400,
                'message': '缺少必要参数',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            return Response({
                'code': 404,
                'message': '标签不存在',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        
        try:
            content_type = ContentType.objects.get(model=content_type_name)
        except ContentType.DoesNotExist:
            return Response({
                'code': 400,
                'message': f'无效的 content_type: {content_type_name}',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 创建或获取关联（避免重复）
        relation, created = TagRelation.objects.get_or_create(
            tag=tag,
            content_type=content_type,
            object_id=object_id
        )
        
        return Response({
            'code': 200,
            'message': '添加成功' if created else '标签已存在',
            'data': {
                'tag_id': tag.id,
                'tag_name': tag.name,
            }
        })
    
    def delete(self, request):
        """移除对象的标签"""
        tag_id = request.data.get('tag_id')
        content_type_name = request.data.get('content_type')
        object_id = request.data.get('object_id')
        
        if not all([tag_id, content_type_name, object_id]):
            return Response({
                'code': 400,
                'message': '缺少必要参数',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            content_type = ContentType.objects.get(model=content_type_name)
        except ContentType.DoesNotExist:
            return Response({
                'code': 400,
                'message': f'无效的 content_type: {content_type_name}',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        deleted_count, _ = TagRelation.objects.filter(
            tag_id=tag_id,
            content_type=content_type,
            object_id=object_id
        ).delete()
        
        return Response({
            'code': 200,
            'message': '移除成功' if deleted_count > 0 else '关联不存在',
            'data': None
        })


# ==================== 知识点管理 ====================
class KnowledgePointManageView(APIView):
    """
    GET  /api/knowledge/points/ - 获取知识点列表（树状结构）
    POST /api/knowledge/points/ - 创建知识点
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """获取知识点树状结构"""
        course_id = request.query_params.get('course_id')
        
        # 获取所有根节点（没有父节点的知识点）
        queryset = KnowledgePoint.objects.filter(parent__isnull=True)
        
        # 按课程过滤
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        
        root_points = queryset.order_by('order', 'id')
        
        def build_tree(point):
            """递归构建树状结构"""
            children = KnowledgePoint.objects.filter(parent=point).order_by('order', 'id')
            return {
                'id': point.id,
                'name': point.name,
                'order': point.order,
                'full_path': point.get_full_path(),
                'children': [build_tree(child) for child in children]
            }
        
        tree = [build_tree(point) for point in root_points]
        
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': {'knowledge_points': tree}
        })
    
    def post(self, request):
        """创建知识点"""
        name = request.data.get('name', '').strip()
        course_id = request.data.get('course_id')
        parent_id = request.data.get('parent_id')
        order = request.data.get('order', 0)
        
        if not name:
            return Response({
                'code': 400,
                'message': '知识点名称不能为空',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if not course_id:
            return Response({
                'code': 400,
                'message': '课程ID不能为空',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 验证课程存在
        from courses.models import Course
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({
                'code': 404,
                'message': '课程不存在',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        
        parent = None
        if parent_id:
            try:
                parent = KnowledgePoint.objects.get(id=parent_id)
            except KnowledgePoint.DoesNotExist:
                return Response({
                    'code': 404,
                    'message': '父知识点不存在',
                    'data': None
                }, status=status.HTTP_404_NOT_FOUND)
        
        point = KnowledgePoint.objects.create(
            name=name,
            course=course,
            parent=parent,
            order=order
        )
        
        return Response({
            'code': 200,
            'message': '创建成功',
            'data': {
                'id': point.id,
                'name': point.name,
                'parent_id': parent.id if parent else None,
                'order': point.order,
                'full_path': point.get_full_path(),
            }
        }, status=status.HTTP_201_CREATED)


class KnowledgePointDetailView(APIView):
    """
    GET    /api/knowledge/points/{id}/ - 获取知识点详情
    PUT    /api/knowledge/points/{id}/ - 更新知识点
    DELETE /api/knowledge/points/{id}/ - 删除知识点
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, point_id):
        """获取知识点详情"""
        try:
            point = KnowledgePoint.objects.get(id=point_id)
        except KnowledgePoint.DoesNotExist:
            return Response({
                'code': 404,
                'message': '知识点不存在',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        
        # 获取子知识点
        children = KnowledgePoint.objects.filter(parent=point).order_by('order')
        
        # 获取关联的对象
        relations = KnowledgePointRelation.objects.filter(
            knowledge_point=point
        ).select_related('content_type')
        
        related_objects = []
        for rel in relations[:50]:
            related_objects.append({
                'content_type': rel.content_type.model,
                'object_id': rel.object_id,
            })
        
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': {
                'id': point.id,
                'name': point.name,
                'parent_id': point.parent.id if point.parent else None,
                'parent_name': point.parent.name if point.parent else None,
                'order': point.order,
                'full_path': point.get_full_path(),
                'children': [
                    {
                        'id': child.id,
                        'name': child.name,
                        'order': child.order,
                    }
                    for child in children
                ],
                'related_count': relations.count(),
                'related_objects': related_objects,
            }
        })
    
    def put(self, request, point_id):
        """更新知识点"""
        try:
            point = KnowledgePoint.objects.get(id=point_id)
        except KnowledgePoint.DoesNotExist:
            return Response({
                'code': 404,
                'message': '知识点不存在',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        
        name = request.data.get('name', '').strip()
        parent_id = request.data.get('parent_id')
        order = request.data.get('order')
        
        if name:
            point.name = name
        
        if parent_id is not None:
            if parent_id == '':
                point.parent = None
            else:
                try:
                    parent = KnowledgePoint.objects.get(id=parent_id)
                    # 防止循环引用
                    if parent.id == point.id:
                        return Response({
                            'code': 400,
                            'message': '不能将知识点设为自己的父节点',
                            'data': None
                        }, status=status.HTTP_400_BAD_REQUEST)
                    point.parent = parent
                except KnowledgePoint.DoesNotExist:
                    return Response({
                        'code': 404,
                        'message': '父知识点不存在',
                        'data': None
                    }, status=status.HTTP_404_NOT_FOUND)
        
        if order is not None:
            point.order = order
        
        point.save()
        
        return Response({
            'code': 200,
            'message': '更新成功',
            'data': {
                'id': point.id,
                'name': point.name,
                'parent_id': point.parent.id if point.parent else None,
                'order': point.order,
                'full_path': point.get_full_path(),
            }
        })
    
    def delete(self, request, point_id):
        """删除知识点（子节点会变成孤儿节点）"""
        try:
            point = KnowledgePoint.objects.get(id=point_id)
        except KnowledgePoint.DoesNotExist:
            return Response({
                'code': 404,
                'message': '知识点不存在',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        
        point.delete()  # 子节点的 parent 会被设为 NULL (on_delete=SET_NULL)
        
        return Response({
            'code': 200,
            'message': '删除成功',
            'data': None
        })


class ObjectKnowledgePointManageView(APIView):
    """
    POST   /api/knowledge/points/attach/ - 给对象关联知识点
    DELETE /api/knowledge/points/detach/ - 移除对象的知识点关联
    GET    /api/knowledge/points/object/ - 获取对象关联的所有知识点
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """获取某个对象关联的所有知识点"""
        content_type_name = request.query_params.get('content_type')  # 如 'course', 'lesson'
        object_id = request.query_params.get('object_id')
        
        if not content_type_name or not object_id:
            return Response({
                'code': 400,
                'message': '缺少参数 content_type 或 object_id',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            content_type = ContentType.objects.get(model=content_type_name)
        except ContentType.DoesNotExist:
            return Response({
                'code': 400,
                'message': f'无效的 content_type: {content_type_name}',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        relations = KnowledgePointRelation.objects.filter(
            content_type=content_type,
            object_id=object_id
        ).select_related('knowledge_point')
        
        points = [
            {
                'id': rel.knowledge_point.id,
                'name': rel.knowledge_point.name,
                'full_path': rel.knowledge_point.get_full_path(),
            }
            for rel in relations
        ]
        
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': {'knowledge_points': points}
        })
    
    def post(self, request):
        """给对象关联知识点"""
        point_id = request.data.get('point_id')
        content_type_name = request.data.get('content_type')  # 如 'course', 'lesson'
        object_id = request.data.get('object_id')
        
        if not all([point_id, content_type_name, object_id]):
            return Response({
                'code': 400,
                'message': '缺少必要参数',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            point = KnowledgePoint.objects.get(id=point_id)
        except KnowledgePoint.DoesNotExist:
            return Response({
                'code': 404,
                'message': '知识点不存在',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        
        try:
            content_type = ContentType.objects.get(model=content_type_name)
        except ContentType.DoesNotExist:
            return Response({
                'code': 400,
                'message': f'无效的 content_type: {content_type_name}',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 创建或获取关联（避免重复）
        relation, created = KnowledgePointRelation.objects.get_or_create(
            knowledge_point=point,
            content_type=content_type,
            object_id=object_id
        )
        
        return Response({
            'code': 200,
            'message': '关联成功' if created else '知识点已关联',
            'data': {
                'point_id': point.id,
                'point_name': point.name,
                'full_path': point.get_full_path(),
            }
        })
    
    def delete(self, request):
        """移除对象的知识点关联"""
        point_id = request.data.get('point_id')
        content_type_name = request.data.get('content_type')
        object_id = request.data.get('object_id')
        
        if not all([point_id, content_type_name, object_id]):
            return Response({
                'code': 400,
                'message': '缺少必要参数',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            content_type = ContentType.objects.get(model=content_type_name)
        except ContentType.DoesNotExist:
            return Response({
                'code': 400,
                'message': f'无效的 content_type: {content_type_name}',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        deleted_count, _ = KnowledgePointRelation.objects.filter(
            knowledge_point_id=point_id,
            content_type=content_type,
            object_id=object_id
        ).delete()
        
        return Response({
            'code': 200,
            'message': '移除成功' if deleted_count > 0 else '关联不存在',
            'data': None
        })
