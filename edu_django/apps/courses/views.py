# courses 应用的视图
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils import timezone
from django.db.models import Count, Q
from datetime import timedelta

from .models import (
    Course, CourseCategory, Chapter, Lesson, 
    CourseTerm, ClassGroup, LessonContentBlock
)
from learning.models import Enrollment

# Create your views here.

# ==================== 公共课程接口 ====================
class PublicCourseListView(APIView):
    """GET /api/courses/ - 获取课程列表"""
    permission_classes = [AllowAny]
    
    def get(self, request):
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('pageSize', 10))
        category_name = request.query_params.get('category')
        keyword = request.query_params.get('keyword')

        queryset = Course.objects.all().select_related('category', 'teacher')
        #展示不用发布，还没实现发布功能
        # queryset = queryset.filter(status='published')

        if category_name:
            queryset = queryset.filter(category__name=category_name)

        if keyword:
            queryset = queryset.filter(
                Q(title__icontains=keyword) | Q(description__icontains=keyword)
            )

        queryset = queryset.annotate(
            enrollment_total=Count('terms__enrollments', distinct=True)
        ).order_by('-created_at')

        total_count = queryset.count()
        total_pages = (total_count + page_size - 1) // page_size if page_size > 0 else 0
        start = (page - 1) * page_size
        end = start + page_size
        courses = queryset[start:end]

        results = []
        for course in courses:
            teacher_name = course.teacher.real_name or course.teacher.nickname or course.teacher.email
            results.append({
                'id': course.id,
                'title': course.title,
                'category': course.category.name if course.category else None,
                'cover': course.cover.url if course.cover else None,
                'price': float(course.price),
                'teacher': {
                    'id': course.teacher.id,
                    'name': teacher_name,
                },
                'enrollment_count': course.enrollment_total,
                'created_at': course.created_at,
            })

        return Response({
            'code': 200,
            'message': '获取成功',
            'data': {
                'results': results,
                'count': total_count,
                'next': page + 1 if page < total_pages else None,
                'previous': page - 1 if page > 1 else None,
                'page': page,
                'pageSize': page_size,
                'totalPages': total_pages
            }
        })


class PublicCourseDetailView(APIView):
    """GET /api/courses/{id}/ - 获取课程详情"""
    permission_classes = [AllowAny]
    
    def get(self, request, pk):
        """获取课程详情，包含章节目录结构"""
        try:
            course = Course.objects.select_related(
                'category', 'teacher'
            ).annotate(
                enrollment_total=Count('terms__enrollments', distinct=True)
            ).get(id=pk)
        except Course.DoesNotExist:
            return Response({
                'code': 404,
                'message': '课程不存在',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        
        # 获取章节目录（只返回一级章节，不含课时详情）
        chapters = Chapter.objects.filter(
            course=course,
            parent__isnull=True
        ).order_by('order', 'id')
        
        chapter_list = []
        for chapter in chapters:
            # 获取该章节下的课时数量
            lesson_count = Lesson.objects.filter(chapter=chapter).count()
            chapter_list.append({
                'id': chapter.id,
                'title': chapter.title,
                'order': chapter.order,
                'lesson_count': lesson_count,
            })
        
        teacher_name = course.teacher.real_name or course.teacher.nickname or course.teacher.email
        
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': {
                'id': course.id,
                'title': course.title,
                'description': course.description,
                'cover': course.cover.url if course.cover else None,
                'price': float(course.price),
                'difficulty': course.difficulty,
                'difficulty_display': course.get_difficulty_display(),
                'status': course.status,
                'teacher': {
                    'id': course.teacher.id,
                    'name': teacher_name,
                },
                'category': course.category.name if course.category else None,
                'enrollment_count': course.enrollment_total,
                'view_count': course.view_count,
                'chapters': chapter_list,
                'created_at': course.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'published_at': course.published_at.strftime('%Y-%m-%d %H:%M:%S') if course.published_at else None,
            }
        })


# class CourseResourcesView(APIView):
#     """GET /api/courses/{id}/resources/ - 获取课程资源"""
#     permission_classes = [AllowAny]
    
#     def get(self, request, pk):
#         # TODO: 实现课程资源查询
#         return Response({
#             'code': 200,
#             'message': '获取成功',
#             'data': {'resources': []}
#         })


class MyCoursesView(APIView):
    """GET /api/courses/my-courses/ - 获取我的课程"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
        查询用户两个身份下的课程：
        1. 作为学生：查询已选课的课程
        2. 作为教师：查询自己创建的课程
        """
        user = request.user
        
        # 1. 查询作为学生选修的课程
        student_enrollments = Enrollment.objects.filter(
            student=user, 
            status='active'
        ).select_related('term__course', 'term__course__category', 'term__course__teacher')
        
        student_courses = []
        for enrollment in student_enrollments:
            course = enrollment.term.course
            teacher_name = course.teacher.real_name or course.teacher.nickname or course.teacher.email
            student_courses.append({
                'id': course.id,
                'title': course.title,
                'category': course.category.name if course.category else None,
                'cover': course.cover.url if course.cover else None,
                'teacher': {
                    'id': course.teacher.id,
                    'name': teacher_name,
                },
                'progress': enrollment.progress,
                'enrollment_id': enrollment.id,
                'created_at': enrollment.created_at,
            })
        
        # 2. 查询作为教师创建的课程
        teacher_courses_qs = Course.objects.filter(
            teacher=user
        ).select_related('category').annotate(
            enrollment_total=Count('terms__enrollments', distinct=True)
        ).order_by('-created_at')
        
        teacher_courses = []
        for course in teacher_courses_qs:
            teacher_courses.append({
                'id': course.id,
                'title': course.title,
                'category': course.category.name if course.category else None,
                'cover': course.cover.url if course.cover else None,
                'price': float(course.price),
                'status': course.status,
                'enrollment_count': course.enrollment_total,
                'created_at': course.created_at,
            })
        
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': {
                'student_courses': student_courses,  # 作为学生选修的课程
                'teacher_courses': teacher_courses,  # 作为教师创建的课程
            }
        })


# ==================== 学生选课和学习 ====================
class CourseEnrollmentView(APIView):
    """
    统一处理选课相关操作：
    GET    /api/courses/{course_id}/enrollment/ - 获取课程的班期和班级信息（供前端选择）
    POST   /api/courses/{course_id}/enrollment/ - 选课（前端传班期、班级信息）
    DELETE /api/courses/{course_id}/enrollment/ - 退课
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, course_id):
        """获取课程的班期和班级信息，供前端选择"""
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({
                'code': 404,
                'message': '课程不存在',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        
        # 获取该课程所有进行中的班期
        terms = CourseTerm.objects.filter(
            course=course,
            status='in_progress'
        ).prefetch_related('class_groups')
        
        terms_data = []
        for term in terms:
            # 获取该班期下的所有班级
            classes = term.class_groups.all()
            classes_data = []
            for class_group in classes:
                # 计算当前班级人数
                current_count = Enrollment.objects.filter(
                    term=term,
                    class_group=class_group,
                    status='active'
                ).count()
                
                classes_data.append({
                    'id': class_group.id,
                    'name': class_group.name,
                    'head_teacher': {
                        'id': class_group.head_teacher.id,
                        'name': class_group.head_teacher.real_name or class_group.head_teacher.nickname
                    } if class_group.head_teacher else None,
                    'current_count': current_count,
                })
            
            # 计算该班期总报名人数
            term_enrollment_count = Enrollment.objects.filter(
                term=term,
                status='active'
            ).count()
            
            # 判断是否已满员
            is_full = False
            if term.enrollment_limit > 0 and term_enrollment_count >= term.enrollment_limit:
                is_full = True
            
            terms_data.append({
                'id': term.id,
                'name': term.name,
                'start_date': term.start_date,
                'end_date': term.end_date,
                # 'description': term.description,
                'enrollment_limit': term.enrollment_limit,
                'current_enrollment': term_enrollment_count,
                'is_full': is_full,
                'classes': classes_data,
            })
        
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': {
                'course_id': course.id,
                'course_title': course.title,
                'price': float(course.price),
                'is_free': course.price == 0,
                'terms': terms_data,
            }
        })
    
    def post(self, request, course_id):
        """选课：前端传入班期ID、班级ID（可选）"""
        user = request.user
        data = request.data
        
        term_id = data.get('term_id')
        class_id = data.get('class_id')  # 可选
        
        if not term_id:
            return Response({
                'code': 400,
                'message': '请选择班期',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # 1. 验证课程和班期
            course = Course.objects.get(id=course_id)
            term = CourseTerm.objects.get(id=term_id, course=course)
            
            # 2. 检查是否已选课
            existing_enrollment = Enrollment.objects.filter(
                student=user,
                term=term
            ).first()
            
            if existing_enrollment:
                if existing_enrollment.status == 'active':
                    return Response({
                        'code': 400,
                        'message': '您已选修该课程',
                        'data': {'enrollment_id': existing_enrollment.id}
                    }, status=status.HTTP_400_BAD_REQUEST)
                else:
                    # 如果之前退课了，重新激活
                    existing_enrollment.status = 'active'
                    existing_enrollment.save()
                    return Response({
                        'code': 200,
                        'message': '选课成功',
                        'data': {
                            'enrollment_id': existing_enrollment.id,
                            'is_free': course.price == 0,
                            'need_payment': course.price > 0,
                        }
                    })
            
            # 3. 检查班期是否满员
            if term.enrollment_limit > 0:
                current_count = Enrollment.objects.filter(
                    term=term,
                    status='active'
                ).count()
                if current_count >= term.enrollment_limit:
                    return Response({
                        'code': 400,
                        'message': '该班期已满员',
                        'data': None
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            # 4. 验证班级（如果传了）
            class_group = None
            if class_id:
                try:
                    class_group = ClassGroup.objects.get(id=class_id, term=term)
                except ClassGroup.DoesNotExist:
                    return Response({
                        'code': 400,
                        'message': '班级不存在或不属于该班期',
                        'data': None
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            # 5. 创建选课记录
            enrollment = Enrollment.objects.create(
                student=user,
                term=term,
                class_group=class_group,
                status='active',
                progress=0.0
            )
            
            # 6. 如果选了班级，将学生加入班级的students多对多关系
            if class_group:
                class_group.students.add(user)
            
            # 7. 判断是否需要支付
            is_free = course.price == 0
            need_payment = course.price > 0
            
            return Response({
                'code': 200,
                'message': '选课成功' if is_free else '请完成支付',
                'data': {
                    'enrollment_id': enrollment.id,
                    'is_free': is_free,
                    'need_payment': need_payment,
                    'price': float(course.price),
                }
            }, status=status.HTTP_201_CREATED)
            
        except Course.DoesNotExist:
            return Response({
                'code': 404,
                'message': '课程不存在',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        except CourseTerm.DoesNotExist:
            return Response({
                'code': 404,
                'message': '班期不存在',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'code': 500,
                'message': f'选课失败: {str(e)}',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self, request, course_id):
        """退课：根据课程ID退出该课程"""
        user = request.user
        
        try:
            course = Course.objects.get(id=course_id)
            
            # 查找该用户在该课程下的选课记录
            enrollment = Enrollment.objects.filter(
                student=user,
                term__course=course,
                status='active'
            ).first()
            
            if not enrollment:
                return Response({
                    'code': 404,
                    'message': '未找到选课记录',
                    'data': None
                }, status=status.HTTP_404_NOT_FOUND)
            
            # 标记为已退课
            enrollment.status = 'dropped'
            enrollment.save()
            
            # 如果有班级，从班级学生列表中移除
            if enrollment.class_group:
                enrollment.class_group.students.remove(user)
            
            return Response({
                'code': 200,
                'message': '退课成功',
                'data': None
            })
            
        except Course.DoesNotExist:
            return Response({
                'code': 404,
                'message': '课程不存在',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'code': 500,
                'message': f'退课失败: {str(e)}',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class StudentCourseDetailView(APIView):
    """GET /api/student/courses/{courseId}/ - 获取课程学习详情"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, course_id):
        # TODO: 实现学习详情查询
        return Response({'code': 200, 'message': '获取成功', 'data': {}})


class StudentCourseProgressView(APIView):
    """POST /api/student/courses/{courseId}/progress/ - 更新学习进度"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, course_id):
        # TODO: 实现学习进度更新（BKT/IRT算法支持）
        return Response({
            'code': 200,
            'message': '更新成功',
            'data': {'progress': 0}
        })


class StudentLessonDetailView(APIView):
    """GET /api/student/courses/{courseId}/lessons/{lessonId}/ - 获取课时详情"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, course_id, lesson_id):
        # TODO: 实现课时详情查询
        return Response({'code': 200, 'message': '获取成功', 'data': {}})


class StudentLessonCompleteView(APIView):
    """POST /api/student/courses/{courseId}/lessons/{lessonId}/complete/ - 完成课时学习"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, course_id, lesson_id):
        # TODO: 实现课时完成逻辑
        return Response({
            'code': 200,
            'message': '课时已完成',
            'data': {}
        })


# ==================== 教师课程管理 ====================
# class TeacherCourseListView(APIView):
#     """GET /api/teacher/courses/ - 获取我教的课程"""
#     permission_classes = [IsAuthenticated]
    
#     def get(self, request):
#         # TODO: 实现教师课程列表查询
#         return Response({
#             'code': 200,
#             'message': '获取成功',
#             'data': {'results': []}
#         })


class TeacherCourseManageView(APIView):
    """
    GET    /api/teacher/courses/{id}/ - 获取课程管理详情
    PUT    /api/teacher/courses/{id}/ - 更新课程
    DELETE /api/teacher/courses/{id}/ - 删除课程
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        """获取课程管理详情"""
        user = request.user
        
        try:
            course = Course.objects.select_related('category').get(
                id=pk,
                teacher=user
            )
        except Course.DoesNotExist:
            return Response({
                'code': 404,
                'message': '课程不存在或您无权访问',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        
        # 统计章节和课时数量
        chapter_count = Chapter.objects.filter(course=course).count()
        lesson_count = Lesson.objects.filter(chapter__course=course).count()
        
        # 统计学生数量
        student_count = Enrollment.objects.filter(
            class_group__term__course=course
        ).count()
        
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': {
                'id': course.id,
                'title': course.title,
                'description': course.description,
                'cover': course.cover.url if course.cover else None,
                'price': float(course.price),
                'difficulty': course.difficulty,
                'difficulty_display': course.get_difficulty_display(),
                'status': course.status,
                'status_display': course.get_status_display(),
                'category': course.category.name if course.category else None,
                'category_id': course.category.id if course.category else None,
                'audit_remark': course.audit_remark,
                'chapter_count': chapter_count,
                'lesson_count': lesson_count,
                'student_count': student_count,
                'view_count': course.view_count,
                'enrollment_count': course.enrollment_count,
                'created_at': course.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'published_at': course.published_at.strftime('%Y-%m-%d %H:%M:%S') if course.published_at else None,
            }
        })
    
    def put(self, request, pk):
        """更新课程信息"""
        user = request.user
        
        try:
            course = Course.objects.get(id=pk, teacher=user)
        except Course.DoesNotExist:
            return Response({
                'code': 404,
                'message': '课程不存在或您无权修改',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        
        data = request.data
        
        # 更新基本信息
        if 'title' in data:
            course.title = data['title'].strip()
        
        if 'description' in data:
            course.description = data['description']
        
        if 'price' in data:
            try:
                course.price = float(data['price'])
            except ValueError:
                return Response({
                    'code': 400,
                    'message': '价格格式不正确',
                    'data': None
                }, status=status.HTTP_400_BAD_REQUEST)
        
        if 'difficulty' in data:
            if data['difficulty'] in ['beginner', 'intermediate', 'advanced']:
                course.difficulty = data['difficulty']
        
        # 更新分类
        if 'category_name' in data:
            category_name = data['category_name']
            if category_name:
                try:
                    category = CourseCategory.objects.get(name=category_name)
                    course.category = category
                except CourseCategory.DoesNotExist:
                    return Response({
                        'code': 400,
                        'message': f'分类"{category_name}"不存在',
                        'data': None
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                course.category = None
        
        course.save()
        
        return Response({
            'code': 200,
            'message': '更新成功',
            'data': {
                'id': course.id,
                'title': course.title,
                'description': course.description,
                'price': float(course.price),
                'difficulty': course.difficulty,
                'category': course.category.name if course.category else None,
            }
        })
    
    def delete(self, request, pk):
        """删除课程（仅草稿状态可删除）"""
        user = request.user
        
        try:
            course = Course.objects.get(id=pk, teacher=user)
        except Course.DoesNotExist:
            return Response({
                'code': 404,
                'message': '课程不存在或您无权删除',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        
        # 只有草稿状态的课程才能删除
        if course.status != 'draft':
            return Response({
                'code': 400,
                'message': f'只有草稿状态的课程可以删除，当前状态：{course.get_status_display()}',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 检查是否有学生选课
        enrollment_count = Enrollment.objects.filter(
            class_group__term__course=course
        ).count()
        
        if enrollment_count > 0:
            return Response({
                'code': 400,
                'message': f'该课程已有{enrollment_count}名学生选课，无法删除',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        course.delete()
        
        return Response({
            'code': 200,
            'message': '删除成功'
        })


class TeacherCourseCreateView(APIView):
    """POST /api/teacher/courses/create - 创建课程"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        创建课程逻辑：
        1. 根据分类名称查找对应的 CourseCategory
        2. 创建课程，默认价格为 0.00（免费），状态为草稿
        3. 自动创建默认班期（不限人数，开课日期为今天，结课日期为一年后）
        4. 自动创建默认班级（不限人数）
        """
        user = request.user
        data = request.data
        
        # 1. 获取必填字段
        title = data.get('title')
        description = data.get('description', '')
        category_name = data.get('category')  # 前端传入分类名称，如“计算机”
        difficulty = data.get('difficulty', 'beginner')
        cover = data.get('cover')  # 可选
        
        if not title:
            return Response({
                'code': 400,
                'message': '课程标题不能为空',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 2. 查找分类（如果前端传了分类名称）
        category = None
        if category_name:
            try:
                category = CourseCategory.objects.get(name=category_name)
            except CourseCategory.DoesNotExist:
                return Response({
                    'code': 400,
                    'message': f'分类 "{category_name}" 不存在',
                    'data': None
                }, status=status.HTTP_400_BAD_REQUEST)
        
        # 3. 创建课程（默认免费，草稿状态）
        try:
            course = Course.objects.create(
                teacher=user,
                category=category,
                title=title,
                description=description,
                price=0.00,  # 默认免费
                difficulty=difficulty,
                status='draft',  # 默认草稿状态
                cover=cover if cover else None
            )
            
            # 4. 创建默认班期（开课日期为今天，结课日期为一年后）
            start_date = timezone.now().date()
            end_date = start_date + timedelta(days=365)
            
            default_term = CourseTerm.objects.create(
                course=course,
                name='默认班期',
                start_date=start_date,
                end_date=end_date,
                description='系统自动创建的默认班期',
                enrollment_limit=0,  # 0 表示不限人数
                status='in_progress'
            )
            
            # 5. 创建默认班级
            ClassGroup.objects.create(
                term=default_term,
                name='默认班级',
                head_teacher=user  # 班主任设为课程创建者
            )
            
            return Response({
                'code': 200,
                'message': '创建成功',
                'data': {
                    'course_id': course.id,
                    'title': course.title,
                    'description': course.description,
                    'status': course.status,
                    'price': float(course.price),
                    'category': category.name if category else None,
                    'default_term_id': default_term.id,
                }
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                'code': 500,
                'message': f'创建失败: {str(e)}',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TeacherCoursePublishView(APIView):
    """POST /api/teacher/courses/{id}/publish/ - 发布课程"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        """发布课程（需检查课程完整性）"""
        user = request.user
        
        try:
            course = Course.objects.get(id=pk, teacher=user)
        except Course.DoesNotExist:
            return Response({
                'code': 404,
                'message': '课程不存在或您无权发布',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        
        # 检查课程状态（只有草稿或被拒绝的课程可以发布）
        if course.status not in ['draft', 'rejected']:
            return Response({
                'code': 400,
                'message': f'当前状态（{course.get_status_display()}）无法发布',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 检查课程完整性
        errors = []
        
        if not course.title or not course.title.strip():
            errors.append('课程标题不能为空')
        
        if not course.description or not course.description.strip():
            errors.append('课程描述不能为空')
        
        if not course.cover:
            errors.append('请上传课程封面')
        
        # 检查是否有章节
        chapter_count = Chapter.objects.filter(course=course).count()
        if chapter_count == 0:
            errors.append('请至少创建一个章节')
        
        # 检查是否有课时
        lesson_count = Lesson.objects.filter(chapter__course=course).count()
        if lesson_count == 0:
            errors.append('请至少创建一个课时')
        
        if errors:
            return Response({
                'code': 400,
                'message': '课程信息不完整',
                'data': {'errors': errors}
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 更新状态为已发布
        course.status = 'published'
        course.published_at = timezone.now()
        course.save()
        
        return Response({
            'code': 200,
            'message': '发布成功',
            'data': {
                'id': course.id,
                'title': course.title,
                'status': course.status,
                'published_at': course.published_at.strftime('%Y-%m-%d %H:%M:%S'),
            }
        })


class TeacherCourseCoverUploadView(APIView):
    """POST /api/teacher/courses/{id}/cover/ - 上传课程封面"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        """
        上传课程封面
        要求：用户必须是该课程的创建者
        """
        user = request.user
        
        # 1. 验证课程存在且属于当前用户
        try:
            course = Course.objects.get(id=pk, teacher=user)
        except Course.DoesNotExist:
            return Response({
                'code': 404,
                'message': '课程不存在或您无权修改该课程',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        
        # 2. 检查是否上传了封面文件
        if 'cover' not in request.FILES:
            return Response({
                'code': 400,
                'message': '请上传封面文件',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 3. 保存封面
        cover_file = request.FILES['cover']
        
        # 验证文件类型（可选）
        allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp']
        if cover_file.content_type not in allowed_types:
            return Response({
                'code': 400,
                'message': '只支持 JPG、PNG、WEBP 格式的图片',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 验证文件大小（可选，限制为5MB）
        if cover_file.size > 5 * 1024 * 1024:
            return Response({
                'code': 400,
                'message': '封面文件不能超过 5MB',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 保存到课程
        course.cover = cover_file
        course.save()
        
        return Response({
            'code': 200,
            'message': '封面上传成功',
            'data': {
                'cover_url': course.cover.url
            }
        })


# ==================== 教师章节管理 ====================
class TeacherChapterManageView(APIView):
    """
    RESTful 章节管理接口：
    GET    /api/teacher/courses/{course_id}/chapters/ - 获取章节目录结构（懒加载，不含课时内容）
    POST   /api/teacher/courses/{course_id}/chapters/ - 创建章节
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, course_id):
        """
        获取课程章节目录结构（懒加载）
        只返回章节和课时的基本信息，不包含课时的具体内容块
        """
        user = request.user
        
        try:
            # 验证课程存在且属于当前用户
            course = Course.objects.get(id=course_id, teacher=user)
        except Course.DoesNotExist:
            return Response({
                'code': 404,
                'message': '课程不存在或您无权访问',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        
        # 获取所有顶级章节（parent=None）
        chapters = Chapter.objects.filter(
            course=course,
            parent=None
        ).prefetch_related('lessons').order_by('order', 'id')
        
        chapters_data = []
        for chapter in chapters:
            # 获取该章节下的所有课时（只返回基本信息）
            lessons = chapter.lessons.all().order_by('order', 'id')
            lessons_data = []
            
            for lesson in lessons:
                lessons_data.append({
                    'id': lesson.id,
                    'title': lesson.title,
                    'order': lesson.order,
                    # 懒加载：不返回 content_blocks
                })
            
            chapters_data.append({
                'id': chapter.id,
                'title': chapter.title,
                'order': chapter.order,
                'lessons': lessons_data,  # 章节下的课时列表（只含基本信息）
            })
        
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': {
                'course_id': course.id,
                'course_title': course.title,
                'teacher_name': course.teacher.real_name,
                'chapters': chapters_data,
            }
        })
    
    def post(self, request, course_id):
        """创建章节"""
        user = request.user
        data = request.data
        
        try:
            # 验证课程存在且属于当前用户
            course = Course.objects.get(id=course_id, teacher=user)
        except Course.DoesNotExist:
            return Response({
                'code': 404,
                'message': '课程不存在或您无权访问',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        
        title = data.get('title')
        order = data.get('order', 0)
        parent_id = data.get('parent_id')  # 可选，支持子章节
        
        if not title:
            return Response({
                'code': 400,
                'message': '章节标题不能为空',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 验证父章节（如果有）
        parent = None
        if parent_id:
            try:
                parent = Chapter.objects.get(id=parent_id, course=course)
            except Chapter.DoesNotExist:
                return Response({
                    'code': 400,
                    'message': '父章节不存在',
                    'data': None
                }, status=status.HTTP_400_BAD_REQUEST)
        
        # 创建章节
        chapter = Chapter.objects.create(
            course=course,
            parent=parent,
            title=title,
            order=order
        )
        
        return Response({
            'code': 200,
            'message': '创建成功',
            'data': {
                'chapter_id': chapter.id,
                'title': chapter.title,
                'order': chapter.order,
            }
        }, status=status.HTTP_201_CREATED)


class TeacherChapterDetailView(APIView):
    """
    RESTful 章节详情接口：
    GET    /api/teacher/courses/{course_id}/chapters/{chapter_id}/ - 获取章节详情
    PUT    /api/teacher/courses/{course_id}/chapters/{chapter_id}/ - 更新章节
    DELETE /api/teacher/courses/{course_id}/chapters/{chapter_id}/ - 删除章节
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, course_id, chapter_id):
        """获取单个章节详情"""
        user = request.user
        
        try:
            course = Course.objects.get(id=course_id, teacher=user)
            chapter = Chapter.objects.get(id=chapter_id, course=course)
        except Course.DoesNotExist:
            return Response({
                'code': 404,
                'message': '课程不存在或您无权访问',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        except Chapter.DoesNotExist:
            return Response({
                'code': 404,
                'message': '章节不存在',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': {
                'id': chapter.id,
                'title': chapter.title,
                'order': chapter.order,
                'parent_id': chapter.parent_id,
            }
        })
    
    def put(self, request, course_id, chapter_id):
        """更新章节信息"""
        user = request.user
        data = request.data
        
        try:
            course = Course.objects.get(id=course_id, teacher=user)
            chapter = Chapter.objects.get(id=chapter_id, course=course)
        except Course.DoesNotExist:
            return Response({
                'code': 404,
                'message': '课程不存在或您无权访问',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        except Chapter.DoesNotExist:
            return Response({
                'code': 404,
                'message': '章节不存在',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        
        # 更新章节字段
        if 'title' in data:
            chapter.title = data['title']
        if 'order' in data:
            chapter.order = data['order']
        
        chapter.save()
        
        return Response({
            'code': 200,
            'message': '更新成功',
            'data': {
                'id': chapter.id,
                'title': chapter.title,
                'order': chapter.order,
            }
        })
    
    def delete(self, request, course_id, chapter_id):
        """删除章节（级联删除课时和内容块）"""
        user = request.user
        
        try:
            course = Course.objects.get(id=course_id, teacher=user)
            chapter = Chapter.objects.get(id=chapter_id, course=course)
        except Course.DoesNotExist:
            return Response({
                'code': 404,
                'message': '课程不存在或您无权访问',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        except Chapter.DoesNotExist:
            return Response({
                'code': 404,
                'message': '章节不存在',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        
        chapter.delete()  # 级联删除关联的课时和内容块
        
        return Response({
            'code': 200,
            'message': '删除成功',
            'data': None
        })


class TeacherChapterSortView(APIView):
    """POST /api/teacher/courses/{course_id}/chapters/sort/ - 批量排序章节"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, course_id):
        """
        批量更新章节排序
        参数: chapters: [{ id: 1, order: 0 }, { id: 2, order: 1 }]
        """
        user = request.user
        data = request.data
        
        try:
            course = Course.objects.get(id=course_id, teacher=user)
        except Course.DoesNotExist:
            return Response({
                'code': 404,
                'message': '课程不存在或您无权访问',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        
        chapters_data = data.get('chapters', [])
        if not chapters_data:
            return Response({
                'code': 400,
                'message': '请提供章节排序数据',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 批量更新排序
        for item in chapters_data:
            chapter_id = item.get('id')
            order = item.get('order')
            
            if chapter_id is not None and order is not None:
                Chapter.objects.filter(
                    id=chapter_id,
                    course=course
                ).update(order=order)
        
        return Response({
            'code': 200,
            'message': '排序成功',
            'data': None
        })


# ==================== 教师课时管理 ====================
class TeacherChapterLessonManageView(APIView):
    """
    章节下的课时管理：
    GET    /api/teacher/courses/{course_id}/chapters/{chapter_id}/lessons/ - 获取章节下的课时列表
    POST   /api/teacher/courses/{course_id}/chapters/{chapter_id}/lessons/ - 创建课时
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, course_id, chapter_id):
        """获取指定章节下的课时列表"""
        user = request.user
        
        try:
            course = Course.objects.get(id=course_id, teacher=user)
            chapter = Chapter.objects.get(id=chapter_id, course=course)
        except Course.DoesNotExist:
            return Response({
                'code': 404,
                'message': '课程不存在或您无权访问',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        except Chapter.DoesNotExist:
            return Response({
                'code': 404,
                'message': '章节不存在',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        
        lessons = Lesson.objects.filter(chapter=chapter).order_by('order', 'id')
        lessons_data = []
        
        for lesson in lessons:
            lessons_data.append({
                'id': lesson.id,
                'title': lesson.title,
                'order': lesson.order,
                'created_at': lesson.created_at,
            })
        
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': {
                'chapter_id': chapter.id,
                'chapter_title': chapter.title,
                'lessons': lessons_data,
            }
        })
    
    def post(self, request, course_id, chapter_id):
        """在指定章节下创建课时"""
        user = request.user
        data = request.data
        
        try:
            course = Course.objects.get(id=course_id, teacher=user)
            chapter = Chapter.objects.get(id=chapter_id, course=course)
        except Course.DoesNotExist:
            return Response({
                'code': 404,
                'message': '课程不存在或您无权访问',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        except Chapter.DoesNotExist:
            return Response({
                'code': 404,
                'message': '章节不存在',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        
        title = data.get('title')
        order = data.get('order', 0)
        
        if not title:
            return Response({
                'code': 400,
                'message': '课时标题不能为空',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 创建课时
        lesson = Lesson.objects.create(
            chapter=chapter,
            title=title,
            order=order
        )
        
        return Response({
            'code': 200,
            'message': '创建成功',
            'data': {
                'lesson_id': lesson.id,
                'title': lesson.title,
                'order': lesson.order,
                'chapter_id': chapter.id,
            }
        }, status=status.HTTP_201_CREATED)


class TeacherLessonDetailView(APIView):
    """
    课时详情管理：
    GET    /api/teacher/courses/{course_id}/lessons/{lesson_id}/ - 获取课时详情（含内容块）
    PUT    /api/teacher/courses/{course_id}/lessons/{lesson_id}/ - 更新课时信息
    DELETE /api/teacher/courses/{course_id}/lessons/{lesson_id}/ - 删除课时
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, course_id, lesson_id):
        """
        获取课时的完整内容（懒加载第二步）
        返回该课时的所有内容块信息
        """
        user = request.user
        
        try:
            # 验证课程存在且属于当前用户
            course = Course.objects.get(id=course_id, teacher=user)
            # 验证课时属于该课程
            lesson = Lesson.objects.select_related('chapter').get(
                id=lesson_id,
                chapter__course=course
            )
        except Course.DoesNotExist:
            return Response({
                'code': 404,
                'message': '课程不存在或您无权访问',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        except Lesson.DoesNotExist:
            return Response({
                'code': 404,
                'message': '课时不存在',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        
        # 获取课时的所有内容块
        content_blocks = lesson.content_blocks.all().order_by('order', 'id')
        blocks_data = []
        
        for block in content_blocks:
            blocks_data.append({
                'id': block.id,
                'type': block.type,
                'type_display': block.get_type_display(),
                'title': block.title,
                'content': block.content,  # JSON 数据
                'file_url': block.file.url if block.file else None,
                'order': block.order,
                'created_at': block.created_at,
            })
        
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': {
                'lesson_id': lesson.id,
                'title': lesson.title,
                'order': lesson.order,
                'chapter_id': lesson.chapter_id,
                'chapter_title': lesson.chapter.title,
                'content_blocks': blocks_data,  # 课时内容块列表
                'created_at': lesson.created_at,
                'updated_at': lesson.updated_at,
            }
        })
    
    def put(self, request, course_id, lesson_id):
        """更新课时信息"""
        user = request.user
        data = request.data
        
        try:
            course = Course.objects.get(id=course_id, teacher=user)
            lesson = Lesson.objects.select_related('chapter').get(
                id=lesson_id,
                chapter__course=course
            )
        except Course.DoesNotExist:
            return Response({
                'code': 404,
                'message': '课程不存在或您无权访问',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        except Lesson.DoesNotExist:
            return Response({
                'code': 404,
                'message': '课时不存在',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        
        # 更新课时字段
        if 'title' in data:
            lesson.title = data['title']
        if 'order' in data:
            lesson.order = data['order']
        
        lesson.save()
        
        return Response({
            'code': 200,
            'message': '更新成功',
            'data': {
                'lesson_id': lesson.id,
                'title': lesson.title,
                'order': lesson.order,
            }
        })
    
    def delete(self, request, course_id, lesson_id):
        """删除课时（级联删除内容块）"""
        user = request.user
        
        try:
            course = Course.objects.get(id=course_id, teacher=user)
            lesson = Lesson.objects.select_related('chapter').get(
                id=lesson_id,
                chapter__course=course
            )
        except Course.DoesNotExist:
            return Response({
                'code': 404,
                'message': '课程不存在或您无权访问',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        except Lesson.DoesNotExist:
            return Response({
                'code': 404,
                'message': '课时不存在',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        
        lesson.delete()  # 级联删除关联的内容块
        
        return Response({
            'code': 200,
            'message': '删除成功',
            'data': None
        })


class TeacherLessonSortView(APIView):
    """POST /api/teacher/courses/{course_id}/chapters/{chapter_id}/lessons/sort/ - 批量排序课时"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, course_id, chapter_id):
        """
        批量更新课时排序
        参数: lessons: [{ id: 1, order: 0 }, { id: 2, order: 1 }]
        """
        user = request.user
        data = request.data
        
        try:
            course = Course.objects.get(id=course_id, teacher=user)
            chapter = Chapter.objects.get(id=chapter_id, course=course)
        except Course.DoesNotExist:
            return Response({
                'code': 404,
                'message': '课程不存在或您无权访问',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        except Chapter.DoesNotExist:
            return Response({
                'code': 404,
                'message': '章节不存在',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        
        lessons_data = data.get('lessons', [])
        if not lessons_data:
            return Response({
                'code': 400,
                'message': '请提供课时排序数据',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 批量更新排序
        for item in lessons_data:
            lesson_id = item.get('id')
            order = item.get('order')
            
            if lesson_id is not None and order is not None:
                Lesson.objects.filter(
                    id=lesson_id,
                    chapter=chapter
                ).update(order=order)
        
        return Response({
            'code': 200,
            'message': '排序成功',
            'data': None
        })


# ==================== 教师内容块管理 ====================
class TeacherContentBlockManageView(APIView):
    """
    POST /api/teacher/courses/{course_id}/lessons/{lesson_id}/content-blocks/ - 批量保存内容块
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request, course_id, lesson_id):
        """
        批量保存课时的内容块（全量保存）
        前端点击"全量保存"按钮时调用
        采用覆盖式保存：删除旧的内容块，创建新的内容块
        """
        user = request.user
        data = request.data
        
        try:
            # 验证课程和课时
            course = Course.objects.get(id=course_id, teacher=user)
            lesson = Lesson.objects.select_related('chapter').get(
                id=lesson_id,
                chapter__course=course
            )
        except Course.DoesNotExist:
            return Response({
                'code': 404,
                'message': '课程不存在或您无权访问',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        except Lesson.DoesNotExist:
            return Response({
                'code': 404,
                'message': '课时不存在',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        
        content_blocks_data = data.get('content_blocks', [])
        
        # 删除该课时的所有旧内容块（覆盖式保存）
        LessonContentBlock.objects.filter(lesson=lesson).delete()
        
        # 批量创建新的内容块
        created_blocks = []
        for block_data in content_blocks_data:
            block_type = block_data.get('type')
            title = block_data.get('title', '')
            content = block_data.get('content')
            file_path = block_data.get('file')  # 文件URL路径
            order = block_data.get('order', 0)
            
            if not block_type:
                continue
            
            # 前端类型映射到后端类型
            # document -> file
            # text -> rich_text
            type_mapping = {
                'document': 'file',
                'text': 'rich_text',
                'video': 'video',
                'image': 'image',
                'code': 'code',
            }
            
            backend_type = type_mapping.get(block_type, block_type)
            
            # 创建内容块
            block = LessonContentBlock.objects.create(
                lesson=lesson,
                type=backend_type,
                title=title,
                content=content,
                order=order
            )
            
            # 如果有文件路径，保存文件字段
            if file_path:
                block.file = str(file_path).replace('/media/', '', 1)
                block.save()
            
            created_blocks.append({
                'id': block.id,
                'type': block.type,
                'title': block.title,
                'order': block.order,
            })
        
        return Response({
            'code': 200,
            'message': '保存成功',
            'data': {
                'lesson_id': lesson.id,
                'content_blocks': created_blocks,
            }
        })


class TeacherContentBlockFileUploadView(APIView):
    """
    POST /api/teacher/courses/{course_id}/lessons/{lesson_id}/content-blocks/upload/ - 上传内容块文件
    支持上传视频、图片、附件等文件资源
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request, course_id, lesson_id):
        """
        上传内容块文件（视频、图片、文档等）
        返回文件URL供前端使用
        """
        user = request.user
        
        try:
            # 验证课程和课时
            course = Course.objects.get(id=course_id, teacher=user)
            lesson = Lesson.objects.select_related('chapter').get(
                id=lesson_id,
                chapter__course=course
            )
        except Course.DoesNotExist:
            return Response({
                'code': 404,
                'message': '课程不存在或您无权访问',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        except Lesson.DoesNotExist:
            return Response({
                'code': 404,
                'message': '课时不存在',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        
        # 检查是否上传了文件
        if 'file' not in request.FILES:
            return Response({
                'code': 400,
                'message': '请上传文件',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        uploaded_file = request.FILES['file']
        file_type = request.data.get('type', 'file')  # video, image, file
        
        # 根据类型验证文件
        if file_type == 'video':
            allowed_types = ['video/mp4', 'video/webm', 'video/ogg', 'video/quicktime']
            max_size = 500 * 1024 * 1024  # 500MB
            if uploaded_file.content_type not in allowed_types:
                return Response({
                    'code': 400,
                    'message': '只支持 MP4、WebM、OGG、MOV 格式的视频',
                    'data': None
                }, status=status.HTTP_400_BAD_REQUEST)
        elif file_type == 'image':
            allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp', 'image/gif']
            max_size = 10 * 1024 * 1024  # 10MB
            if uploaded_file.content_type not in allowed_types:
                return Response({
                    'code': 400,
                    'message': '只支持 JPG、PNG、WebP、GIF 格式的图片',
                    'data': None
                }, status=status.HTTP_400_BAD_REQUEST)
        else:  # file (文档、附件等)
            allowed_types = [
                'application/pdf',
                'application/msword',
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                'application/vnd.ms-excel',
                'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                'application/vnd.ms-powerpoint',
                'application/vnd.openxmlformats-officedocument.presentationml.presentation',
                'application/zip',
                'application/x-rar-compressed',
                'text/plain',
            ]
            max_size = 50 * 1024 * 1024  # 50MB
            # 文件类型比较宽松，只检查大小
        
        # 验证文件大小
        if uploaded_file.size > max_size:
            return Response({
                'code': 400,
                'message': f'文件大小不能超过 {max_size // (1024 * 1024)}MB',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 创建临时内容块或直接返回文件URL
        # 方案1：直接保存文件并返回URL（推荐，前端后续批量保存时使用）
        from django.core.files.storage import default_storage
        from django.utils import timezone
        import os
        
        # 生成文件路径
        now = timezone.now()
        file_extension = os.path.splitext(uploaded_file.name)[1]
        file_path = f'lessons/files/{now.year}/{now.month:02d}/{lesson.id}_{now.timestamp()}{file_extension}'
        
        # 保存文件
        saved_path = default_storage.save(file_path, uploaded_file)
        
        print(f"文件已保存: {saved_path}")
        
        return Response({
            'code': 200,
            'message': '上传成功',
            'data': {
                'file_path': saved_path, # 给后端保存内容块用
                'file_name': uploaded_file.name,
                'file_size': uploaded_file.size,
                'file_type': file_type,
            }
        })


# ==================== 教师学生管理 ====================
class TeacherCourseStudentListView(APIView):
    """GET /api/teacher/courses/{courseId}/students/ - 获取课程学生列表"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, course_id):
        # TODO: 实现学生列表查询
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': {'results': []}
        })


class TeacherStudentProgressView(APIView):
    """GET /api/teacher/courses/{courseId}/students/{studentId}/progress/ - 获取学生学习进度"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, course_id, student_id):
        # TODO: 实现学生进度查询
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': {}
        })


# ==================== 班级与学期管理 ====================
class TeacherTermManageView(APIView):
    """
    GET  /api/teacher/courses/{courseId}/terms/ - 获取学期列表
    POST /api/teacher/courses/{courseId}/terms/ - 创建学期
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, course_id):
        # TODO: 实现学期列表查询
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': {'terms': []}
        })
    
    def post(self, request, course_id):
        # TODO: 实现学期创建
        return Response({
            'code': 200,
            'message': '创建成功',
            'data': {'term_id': None}
        }, status=status.HTTP_201_CREATED)


class TeacherTermDetailView(APIView):
    """
    PUT    /api/teacher/courses/{courseId}/terms/{id}/ - 更新学期
    DELETE /api/teacher/courses/{courseId}/terms/{id}/ - 删除学期
    """
    permission_classes = [IsAuthenticated]
    
    def put(self, request, course_id, term_id):
        # TODO: 实现学期更新
        return Response({
            'code': 200,
            'message': '更新成功',
            'data': {}
        })
    
    def delete(self, request, course_id, term_id):
        # TODO: 实现学期删除
        return Response({
            'code': 200,
            'message': '删除成功'
        })


class TeacherClassManageView(APIView):
    """
    GET  /api/teacher/courses/{courseId}/classes/ - 获取班级列表
    POST /api/teacher/courses/{courseId}/classes/ - 创建班级
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, course_id):
        # TODO: 实现班级列表查询
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': {'classes': []}
        })
    
    def post(self, request, course_id):
        # TODO: 实现班级创建
        return Response({
            'code': 200,
            'message': '创建成功',
            'data': {'class_id': None}
        }, status=status.HTTP_201_CREATED)


class TeacherClassDetailView(APIView):
    """
    PUT    /api/teacher/courses/{courseId}/classes/{id}/ - 更新班级
    DELETE /api/teacher/courses/{courseId}/classes/{id}/ - 删除班级
    """
    permission_classes = [IsAuthenticated]
    
    def put(self, request, course_id, class_id):
        # TODO: 实现班级更新
        return Response({
            'code': 200,
            'message': '更新成功',
            'data': {}
        })
    
    def delete(self, request, course_id, class_id):
        # TODO: 实现班级删除
        return Response({
            'code': 200,
            'message': '删除成功'
        })


# ==================== 数据统计 ====================
class TeacherCourseStatisticsView(APIView):
    """GET /api/teacher/courses/{courseId}/statistics/ - 获取课程统计数据"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, course_id):
        # TODO: 实现课程统计查询（学习分析）
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': {}
        })


class TeacherDashboardView(APIView):
    """GET /api/teacher/dashboard/ - 获取教师仪表板数据"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # TODO: 实现仪表板数据查询
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': {}
        })
