# exams 应用的视图
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType

from .models import QuestionBank, ExamPaper, ExamSession, ExamSubmission
from courses.models import Course
from knowledge.models import Tag, KnowledgePoint, KnowledgePointRelation, TagRelation, QuestionCategory

# Create your views here.

# ==================== 题目文件夹管理 ====================
class TeacherQuestionCategoryManageView(APIView):
    """
    GET  /api/teacher/courses/{course_id}/question-categories/ - 获取文件夹树
    POST /api/teacher/courses/{course_id}/question-categories/ - 创建文件夹
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, course_id):
        """获取文件夹树状结构"""
        user = request.user
        
        try:
            course = Course.objects.get(id=course_id, teacher=user)
        except Course.DoesNotExist:
            return Response({
                'code': 404,
                'message': '课程不存在或您无权访问',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        
        # 获取所有未删除的根文件夹
        root_categories = QuestionCategory.objects.filter(
            course=course,
            parent__isnull=True,
            is_deleted=False
        ).order_by('order', 'id')
        
        def build_tree(category):
            """递归构建树状结构"""
            children = QuestionCategory.objects.filter(
                parent=category,
                is_deleted=False
            ).order_by('order', 'id')
            
            # 统计该文件夹下的题目数量（不含子文件夹）
            question_count = QuestionBank.objects.filter(
                category=category,
                is_deleted=False
            ).count()
            
            return {
                'id': category.id,
                'name': category.name,
                'order': category.order,
                'question_count': question_count,
                'children': [build_tree(child) for child in children]
            }
        
        tree = [build_tree(cat) for cat in root_categories]
        
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': {'categories': tree}
        })
    
    def post(self, request, course_id):
        """创建文件夹"""
        user = request.user
        
        try:
            course = Course.objects.get(id=course_id, teacher=user)
        except Course.DoesNotExist:
            return Response({
                'code': 404,
                'message': '课程不存在或您无权访问',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        
        data = request.data
        name = data.get('name', '').strip()
        parent_id = data.get('parent_id')
        order = data.get('order', 0)
        
        if not name:
            return Response({
                'code': 400,
                'message': '文件夹名称不能为空',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 验证父文件夹
        parent = None
        if parent_id:
            try:
                parent = QuestionCategory.objects.get(
                    id=parent_id,
                    course=course,
                    is_deleted=False
                )
            except QuestionCategory.DoesNotExist:
                return Response({
                    'code': 404,
                    'message': '父文件夹不存在',
                    'data': None
                }, status=status.HTTP_404_NOT_FOUND)
        
        category = QuestionCategory.objects.create(
            course=course,
            name=name,
            parent=parent,
            order=order
        )
        
        return Response({
            'code': 200,
            'message': '创建成功',
            'data': {
                'id': category.id,
                'name': category.name,
                'parent_id': parent.id if parent else None,
                'order': category.order,
            }
        }, status=status.HTTP_201_CREATED)


class TeacherQuestionCategoryDetailView(APIView):
    """
    GET    /api/teacher/courses/{course_id}/question-categories/{category_id}/ - 获取文件夹详情
    PUT    /api/teacher/courses/{course_id}/question-categories/{category_id}/ - 更新文件夹
    DELETE /api/teacher/courses/{course_id}/question-categories/{category_id}/ - 删除文件夹（软删除）
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, course_id, category_id):
        """获取文件夹详情"""
        user = request.user
        
        try:
            course = Course.objects.get(id=course_id, teacher=user)
            category = QuestionCategory.objects.get(
                id=category_id,
                course=course,
                is_deleted=False
            )
        except (Course.DoesNotExist, QuestionCategory.DoesNotExist):
            return Response({
                'code': 404,
                'message': '文件夹不存在或您无权访问',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        
        # 获取子文件夹
        children = QuestionCategory.objects.filter(
            parent=category,
            is_deleted=False
        ).order_by('order')
        
        # 统计题目数量
        question_count = QuestionBank.objects.filter(
            category=category,
            is_deleted=False
        ).count()
        
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': {
                'id': category.id,
                'name': category.name,
                'parent_id': category.parent.id if category.parent else None,
                'order': category.order,
                'question_count': question_count,
                'children': [
                    {
                        'id': child.id,
                        'name': child.name,
                        'order': child.order,
                    } for child in children
                ],
                'created_at': category.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            }
        })
    
    def put(self, request, course_id, category_id):
        """更新文件夹"""
        user = request.user
        
        try:
            course = Course.objects.get(id=course_id, teacher=user)
            category = QuestionCategory.objects.get(
                id=category_id,
                course=course,
                is_deleted=False
            )
        except (Course.DoesNotExist, QuestionCategory.DoesNotExist):
            return Response({
                'code': 404,
                'message': '文件夹不存在或您无权访问',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        
        data = request.data
        
        if 'name' in data:
            name = data['name'].strip()
            if not name:
                return Response({
                    'code': 400,
                    'message': '文件夹名称不能为空',
                    'data': None
                }, status=status.HTTP_400_BAD_REQUEST)
            category.name = name
        
        if 'parent_id' in data:
            if data['parent_id'] is None or data['parent_id'] == '':
                category.parent = None
            else:
                try:
                    parent = QuestionCategory.objects.get(
                        id=data['parent_id'],
                        course=course,
                        is_deleted=False
                    )
                    # 防止循环引用
                    if parent.id == category.id:
                        return Response({
                            'code': 400,
                            'message': '不能将文件夹设为自己的父文件夹',
                            'data': None
                        }, status=status.HTTP_400_BAD_REQUEST)
                    category.parent = parent
                except QuestionCategory.DoesNotExist:
                    return Response({
                        'code': 404,
                        'message': '父文件夹不存在',
                        'data': None
                    }, status=status.HTTP_404_NOT_FOUND)
        
        if 'order' in data:
            category.order = data['order']
        
        category.save()
        
        return Response({
            'code': 200,
            'message': '更新成功',
            'data': {
                'id': category.id,
                'name': category.name,
                'parent_id': category.parent.id if category.parent else None,
                'order': category.order,
            }
        })
    
    def delete(self, request, course_id, category_id):
        """删除文件夹（软删除，级联软删除子文件夹和题目）"""
        user = request.user
        
        try:
            course = Course.objects.get(id=course_id, teacher=user)
            category = QuestionCategory.objects.get(
                id=category_id,
                course=course,
                is_deleted=False
            )
        except (Course.DoesNotExist, QuestionCategory.DoesNotExist):
            return Response({
                'code': 404,
                'message': '文件夹不存在或您无权访问',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        
        # 递归软删除该文件夹及其所有子文件夹和题目
        def soft_delete_category(cat):
            # 软删除该文件夹下的所有题目
            QuestionBank.objects.filter(category=cat).update(is_deleted=True)
            
            # 递归软删除子文件夹
            children = QuestionCategory.objects.filter(parent=cat, is_deleted=False)
            for child in children:
                soft_delete_category(child)
            
            # 软删除当前文件夹
            cat.is_deleted = True
            cat.save()
        
        soft_delete_category(category)
        
        return Response({
            'code': 200,
            'message': '删除成功',
            'data': None
        })


# ==================== 题库管理 ====================
class TeacherQuestionBankManageView(APIView):
    """
    GET  /api/teacher/courses/{course_id}/questions/ - 获取题库列表
    POST /api/teacher/courses/{course_id}/questions/ - 创建题目
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, course_id):
        """获取题库列表（支持分页、筛选）"""
        user = request.user
        
        # 验证课程权限
        try:
            course = Course.objects.get(id=course_id, teacher=user)
        except Course.DoesNotExist:
            return Response({
                'code': 404,
                'message': '课程不存在或您无权访问',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        
        # 筛选参数
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('pageSize', 20))
        question_type = request.query_params.get('type')
        keyword = request.query_params.get('keyword', '')
        tag_id = request.query_params.get('tag_id')
        point_id = request.query_params.get('point_id')
        category_id = request.query_params.get('category_id')  # 文件夹ID
        
        queryset = QuestionBank.objects.filter(course=course, is_deleted=False)
        
        if question_type:
            queryset = queryset.filter(type=question_type)
        
        # 按文件夹筛选（默认只返回根目录的题目）
        if category_id is None or category_id == '' or category_id == '0' or category_id == 'null':
            # 未传参数或明确指定根目录，返回未分类题目
            queryset = queryset.filter(category__isnull=True)
        else:
            # 返回指定文件夹下的题目
            queryset = queryset.filter(category_id=category_id)
        
        if keyword:
            queryset = queryset.filter(
                Q(title__icontains=keyword) | Q(content__icontains=keyword)
            )
        
        # 按标签筛选
        if tag_id:
            content_type = ContentType.objects.get_for_model(QuestionBank)
            tagged_question_ids = TagRelation.objects.filter(
                tag_id=tag_id,
                content_type=content_type
            ).values_list('object_id', flat=True)
            queryset = queryset.filter(id__in=tagged_question_ids)
        
        # 按知识点筛选
        if point_id:
            content_type = ContentType.objects.get_for_model(QuestionBank)
            pointed_question_ids = KnowledgePointRelation.objects.filter(
                knowledge_point_id=point_id,
                content_type=content_type
            ).values_list('object_id', flat=True)
            queryset = queryset.filter(id__in=pointed_question_ids)
        
        total = queryset.count()
        start = (page - 1) * page_size
        end = start + page_size
        questions = queryset.order_by('-created_at')[start:end]
        
        # 获取题目的标签和知识点
        content_type = ContentType.objects.get_for_model(QuestionBank)
        question_list = []
        
        for q in questions:
            # 获取标签
            tags = TagRelation.objects.filter(
                content_type=content_type,
                object_id=q.id
            ).select_related('tag')
            
            # 获取知识点
            points = KnowledgePointRelation.objects.filter(
                content_type=content_type,
                object_id=q.id
            ).select_related('knowledge_point')
            
            question_list.append({
                'id': q.id,
                'title': q.title,
                'type': q.type,
                'type_display': q.get_type_display(),
                'difficulty': q.difficulty,
                'content': q.content,
                'category_id': q.category.id if q.category else None,
                'category_name': q.category.name if q.category else '未分类',
                'creator': q.created_by.real_name if q.created_by else '未知',
                'tags': [{'id': t.tag.id, 'name': t.tag.name} for t in tags],
                'knowledge_points': [
                    {
                        'id': p.knowledge_point.id,
                        'name': p.knowledge_point.name,
                        'full_path': p.knowledge_point.get_full_path()
                    } for p in points
                ],
                'created_at': q.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            })
        
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': {
                'questions': question_list,
                'total': total,
                'page': page,
                'pageSize': page_size,
            }
        })
    
    def post(self, request, course_id):
        """创建题目"""
        user = request.user
        
        # 验证课程权限
        try:
            course = Course.objects.get(id=course_id, teacher=user)
        except Course.DoesNotExist:
            return Response({
                'code': 404,
                'message': '课程不存在或您无权访问',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        
        data = request.data
        title = data.get('title', '').strip()
        question_type = data.get('type')
        content = data.get('content')
        difficulty = data.get('difficulty', 0.5)
        category_id = data.get('category_id')
        tag_ids = data.get('tag_ids', [])
        point_ids = data.get('point_ids', [])
        
        if not title or not question_type or not content:
            return Response({
                'code': 400,
                'message': '题目名称、类型和内容不能为空',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 验证文件夹（如果提供）
        category = None
        if category_id is not None and category_id != '' and category_id != 'null':
            try:
                category = QuestionCategory.objects.get(
                    id=category_id,
                    course=course,
                    is_deleted=False
                )
            except QuestionCategory.DoesNotExist:
                return Response({
                    'code': 404,
                    'message': '文件夹不存在',
                    'data': None
                }, status=status.HTTP_404_NOT_FOUND)
        
        # 创建题目
        question = QuestionBank.objects.create(
            course=course,
            title=title,
            type=question_type,
            content=content,
            difficulty=difficulty,
            category=category,
            created_by=user
        )
        
        return Response({
            'code': 200,
            'message': '创建成功',
            'data': {
                'id': question.id,
                'title': question.title,
                'type': question.type,
                'creator': user.real_name
            }
        }, status=status.HTTP_201_CREATED)


class TeacherQuestionBankDetailView(APIView):
    """
    GET    /api/teacher/courses/{course_id}/questions/{question_id}/ - 获取题目详情
    PUT    /api/teacher/courses/{course_id}/questions/{question_id}/ - 更新题目
    DELETE /api/teacher/courses/{course_id}/questions/{question_id}/ - 删除题目
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, course_id, question_id):
        """获取题目详情"""
        user = request.user
        
        try:
            course = Course.objects.get(id=course_id, teacher=user)
            question = QuestionBank.objects.get(id=question_id, course=course)
        except (Course.DoesNotExist, QuestionBank.DoesNotExist):
            return Response({
                'code': 404,
                'message': '题目不存在或您无权访问',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        
        # 获取标签和知识点
        content_type = ContentType.objects.get_for_model(QuestionBank)
        
        tags = TagRelation.objects.filter(
            content_type=content_type,
            object_id=question.id
        ).select_related('tag')
        
        points = KnowledgePointRelation.objects.filter(
            content_type=content_type,
            object_id=question.id
        ).select_related('knowledge_point')
        
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': {
                'id': question.id,
                'title': question.title,
                'type': question.type,
                'type_display': question.get_type_display(),
                'content': question.content,
                'difficulty': question.difficulty,
                'category_id': question.category.id if question.category else None,
                'category_name': question.category.name if question.category else '未分类',
                'creator': question.created_by.real_name if question.created_by else '未知',
                'tags': [{'id': t.tag.id, 'name': t.tag.name} for t in tags],
                'knowledge_points': [
                    {
                        'id': p.knowledge_point.id,
                        'name': p.knowledge_point.name,
                        'full_path': p.knowledge_point.get_full_path()
                    } for p in points
                ],
                'created_at': question.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            }
        })
    
    def put(self, request, course_id, question_id):
        """更新题目"""
        user = request.user
        
        try:
            course = Course.objects.get(id=course_id, teacher=user)
            question = QuestionBank.objects.get(id=question_id, course=course)
        except (Course.DoesNotExist, QuestionBank.DoesNotExist):
            return Response({
                'code': 404,
                'message': '题目不存在或您无权访问',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        
        data = request.data
        
        if 'title' in data:
            question.title = data['title'].strip()
        if 'type' in data:
            question.type = data['type']
        if 'content' in data:
            question.content = data['content']
        if 'difficulty' in data:
            question.difficulty = data['difficulty']
        
        # 更新文件夹
        if 'category_id' in data:
            category_id = data['category_id']
            if category_id is None or category_id == '' or category_id == 'null':
                question.category = None
            else:
                try:
                    category = QuestionCategory.objects.get(
                        id=category_id,
                        course=course,
                        is_deleted=False
                    )
                    question.category = category
                except QuestionCategory.DoesNotExist:
                    return Response({
                        'code': 404,
                        'message': '文件夹不存在',
                        'data': None
                    }, status=status.HTTP_404_NOT_FOUND)
        
        question.save()
        
        # 更新标签关联
        if 'tag_ids' in data:
            content_type = ContentType.objects.get_for_model(QuestionBank)
            TagRelation.objects.filter(
                content_type=content_type,
                object_id=question.id
            ).delete()
            
            for tag_id in data['tag_ids']:
                try:
                    tag = Tag.objects.get(id=tag_id, course=course)
                    TagRelation.objects.create(
                        tag=tag,
                        content_type=content_type,
                        object_id=question.id
                    )
                except Tag.DoesNotExist:
                    pass
        
        # 更新知识点关联
        if 'point_ids' in data:
            content_type = ContentType.objects.get_for_model(QuestionBank)
            KnowledgePointRelation.objects.filter(
                content_type=content_type,
                object_id=question.id
            ).delete()
            
            for point_id in data['point_ids']:
                try:
                    point = KnowledgePoint.objects.get(id=point_id, course=course)
                    KnowledgePointRelation.objects.create(
                        knowledge_point=point,
                        content_type=content_type,
                        object_id=question.id
                    )
                except KnowledgePoint.DoesNotExist:
                    pass
        
        return Response({
            'code': 200,
            'message': '更新成功',
            'data': {
                'id': question.id,
                'title': question.title,
            }
        })
    
    def delete(self, request, course_id, question_id):
        """删除题目（软删除）"""
        user = request.user
        
        try:
            course = Course.objects.get(id=course_id, teacher=user)
            question = QuestionBank.objects.get(id=question_id, course=course)
        except (Course.DoesNotExist, QuestionBank.DoesNotExist):
            return Response({
                'code': 404,
                'message': '题目不存在或您无权访问',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        
        # 软删除
        question.is_deleted = True
        question.save()
        
        return Response({
            'code': 200,
            'message': '删除成功',
            'data': None
        })


# ==================== 学生考试 ====================
class StudentExamListView(APIView):
    """GET /api/student/exams/ - 获取考试列表"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # TODO: 实现考试列表查询
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': {'results': []}
        })


class StudentExamDetailView(APIView):
    """GET /api/student/courses/{courseId}/exams/{examId}/ - 获取考试详情"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, course_id, exam_id):
        # TODO: 实现考试详情查询
        return Response({'code': 200, 'message': '获取成功', 'data': {}})


class StudentExamStartView(APIView):
    """POST /api/student/courses/{courseId}/exams/{examId}/start/ - 开始考试"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, course_id, exam_id):
        # TODO: 实现考试启动
        return Response({
            'code': 200,
            'message': '考试已开始',
            'data': {'session_id': None}
        })


class StudentExamSubmitView(APIView):
    """POST /api/student/courses/{courseId}/exams/{examId}/submit/ - 提交答卷"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, course_id, exam_id):
        # TODO: 实现答卷提交（Auto-Grading支持）
        return Response({
            'code': 200,
            'message': '提交成功',
            'data': {'submission_id': None}
        }, status=status.HTTP_201_CREATED)


class StudentExamResultView(APIView):
    """GET /api/student/courses/{courseId}/exams/{examId}/result/ - 获取考试成绩"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, course_id, exam_id):
        # TODO: 实现考试成绩查询
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': {}
        })


# ==================== 教师试卷管理 ====================
class TeacherExamManageView(APIView):
    """
    GET  /api/teacher/courses/{course_id}/exams/ - 获取试卷列表
    POST /api/teacher/courses/{course_id}/exams/ - 创建试卷
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, course_id):
        """获取试卷列表"""
        user = request.user
        
        try:
            course = Course.objects.get(id=course_id, teacher=user)
        except Course.DoesNotExist:
            return Response({
                'code': 404,
                'message': '课程不存在或您无权访问',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('pageSize', 20))
        
        queryset = ExamPaper.objects.filter(course=course).order_by('-created_at')
        
        total = queryset.count()
        start = (page - 1) * page_size
        end = start + page_size
        papers = queryset[start:end]
        
        paper_list = [
            {
                'id': p.id,
                'title': p.title,
                'total_score': p.total_score,
                'duration': p.duration,
                'status': p.status,
                'question_count': p.questions.count(),
                'created_at': p.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            }
            for p in papers
        ]
        
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': {
                'exams': paper_list,
                'total': total,
                'page': page,
                'pageSize': page_size,
            }
        })
    
    def post(self, request, course_id):
        """创建试卷"""
        user = request.user
        
        try:
            course = Course.objects.get(id=course_id, teacher=user)
        except Course.DoesNotExist:
            return Response({
                'code': 404,
                'message': '课程不存在或您无权访问',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        
        data = request.data
        title = data.get('title', '').strip()
        total_score = data.get('total_score', 100)
        duration = data.get('duration', 90)
        question_ids = data.get('question_ids', [])
        
        if not title:
            return Response({
                'code': 400,
                'message': '试卷标题不能为空',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        paper = ExamPaper.objects.create(
            course=course,
            title=title,
            total_score=total_score,
            duration=duration
        )
        
        # 关联题目
        if question_ids:
            questions = QuestionBank.objects.filter(
                id__in=question_ids,
                course=course,
                is_deleted=False
            )
            paper.questions.set(questions)
        
        return Response({
            'code': 200,
            'message': '创建成功',
            'data': {
                'id': paper.id,
                'title': paper.title,
            }
        }, status=status.HTTP_201_CREATED)


class TeacherExamPaperDetailView(APIView):
    """
    GET    /api/teacher/courses/{course_id}/exams/{exam_id}/ - 获取试卷详情
    PUT    /api/teacher/courses/{course_id}/exams/{exam_id}/ - 更新试卷
    DELETE /api/teacher/courses/{course_id}/exams/{exam_id}/ - 删除试卷
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, course_id, exam_id):
        """获取试卷详情"""
        user = request.user
        
        try:
            course = Course.objects.get(id=course_id, teacher=user)
            paper = ExamPaper.objects.get(id=exam_id, course=course)
        except (Course.DoesNotExist, ExamPaper.DoesNotExist):
            return Response({
                'code': 404,
                'message': '试卷不存在或您无权访问',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        
        # 获取题目列表
        questions = paper.questions.filter(is_deleted=False)
        question_list = [
            {
                'id': q.id,
                'title': q.title,
                'type': q.type,
                'type_display': q.get_type_display(),
                'difficulty': q.difficulty,
            }
            for q in questions
        ]
        
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': {
                'id': paper.id,
                'title': paper.title,
                'total_score': paper.total_score,
                'duration': paper.duration,
                'status': paper.status,
                'questions': question_list,
                'created_at': paper.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            }
        })
    
    def put(self, request, course_id, exam_id):
        """更新试卷"""
        user = request.user
        
        try:
            course = Course.objects.get(id=course_id, teacher=user)
            paper = ExamPaper.objects.get(id=exam_id, course=course)
        except (Course.DoesNotExist, ExamPaper.DoesNotExist):
            return Response({
                'code': 404,
                'message': '试卷不存在或您无权访问',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        
        data = request.data
        
        if 'title' in data:
            paper.title = data['title'].strip()
        if 'total_score' in data:
            paper.total_score = data['total_score']
        if 'duration' in data:
            paper.duration = data['duration']
        
        paper.save()
        
        # 更新题目关联
        if 'question_ids' in data:
            questions = QuestionBank.objects.filter(
                id__in=data['question_ids'],
                course=course,
                is_deleted=False
            )
            paper.questions.set(questions)
        
        return Response({
            'code': 200,
            'message': '更新成功',
            'data': {
                'id': paper.id,
                'title': paper.title,
            }
        })
    
    def delete(self, request, course_id, exam_id):
        """删除试卷"""
        user = request.user
        
        try:
            course = Course.objects.get(id=course_id, teacher=user)
            paper = ExamPaper.objects.get(id=exam_id, course=course)
        except (Course.DoesNotExist, ExamPaper.DoesNotExist):
            return Response({
                'code': 404,
                'message': '试卷不存在或您无权访问',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        
        paper.delete()
        
        return Response({
            'code': 200,
            'message': '删除成功',
            'data': None
        })


class TeacherExamPublishView(APIView):
    """POST /api/teacher/courses/{course_id}/exams/{exam_id}/publish/ - 发布试卷"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, course_id, exam_id):
        """发布试卷"""
        user = request.user
        
        try:
            course = Course.objects.get(id=course_id, teacher=user)
            paper = ExamPaper.objects.get(id=exam_id, course=course)
        except (Course.DoesNotExist, ExamPaper.DoesNotExist):
            return Response({
                'code': 404,
                'message': '试卷不存在或您无权访问',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        
        if paper.questions.count() == 0:
            return Response({
                'code': 400,
                'message': '试卷至少需要包含一道题目',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        paper.status = 'published'
        paper.save()
        
        return Response({
            'code': 200,
            'message': '发布成功',
            'data': {
                'id': paper.id,
                'status': paper.status,
            }
        })


# ==================== 旧版本兼容视图（待删除） ====================
class TeacherExamListView(APIView):
    """GET /api/teacher/exams/ - 获取试卷库"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # TODO: 实现试卷库列表查询
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': {'results': []}
        })


class TeacherExamDetailView(APIView):
    """GET /api/teacher/exams/{id}/ - 获取试卷详情"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        # TODO: 实现试卷详情查询
        return Response({'code': 200, 'message': '获取成功', 'data': {}})


class TeacherExamCreateView(APIView):
    """POST /api/teacher/exams/ - 创建试卷"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # TODO: 实现试卷创建
        return Response({
            'code': 200,
            'message': '创建成功',
            'data': {'exam_id': None}
        }, status=status.HTTP_201_CREATED)


class TeacherExamUpdateView(APIView):
    """PUT /api/teacher/exams/{id}/ - 更新试卷"""
    permission_classes = [IsAuthenticated]
    
    def put(self, request, pk):
        # TODO: 实现试卷更新
        return Response({
            'code': 200,
            'message': '更新成功',
            'data': {}
        })


class TeacherExamDeleteView(APIView):
    """DELETE /api/teacher/exams/{id}/ - 删除试卷"""
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, pk):
        # TODO: 实现试卷删除
        return Response({
            'code': 200,
            'message': '删除成功'
        })


class TeacherExamPublishView(APIView):
    """POST /api/teacher/exams/{id}/publish/ - 发布试卷"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        # TODO: 实现试卷发布
        return Response({
            'code': 200,
            'message': '发布成功',
            'data': {}
        })


class TeacherExamSubmissionsView(APIView):
    """GET /api/teacher/exams/{id}/submissions/ - 获取考试提交列表"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        # TODO: 实现提交列表查询
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': {'results': []}
        })


class TeacherExamGradeView(APIView):
    """POST /api/teacher/exams/{exam_id}/submissions/{submission_id}/grade/ - 批改试卷"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, exam_id, submission_id):
        # TODO: 实现试卷批改（Auto-Grading支持）
        return Response({
            'code': 200,
            'message': '批改成功',
            'data': {}
        })


class StudentExamSubmitView(APIView):
    """提交考试 - POST Auto-Grading交卷触发自动阅卷"""
    pass
