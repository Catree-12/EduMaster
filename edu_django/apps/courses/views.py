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
    CourseTerm, ClassGroup
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
        # TODO: 实现课程详情查询
        return Response({'code': 200, 'message': '获取成功', 'data': {}})


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


class TeacherCourseDetailView(APIView):
    """GET /api/teacher/courses/{id}/ - 获取课程管理详情"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        # TODO: 实现课程管理详情查询
        return Response({'code': 200, 'message': '获取成功', 'data': {}})


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


class TeacherCourseUpdateView(APIView):
    """PUT /api/teacher/courses/{id}/ - 更新课程"""
    permission_classes = [IsAuthenticated]
    
    def put(self, request, pk):
        # TODO: 实现课程更新
        return Response({
            'code': 200,
            'message': '更新成功',
            'data': {}
        })


class TeacherCourseDeleteView(APIView):
    """DELETE /api/teacher/courses/{id}/ - 删除课程"""
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, pk):
        # TODO: 实现课程删除
        return Response({
            'code': 200,
            'message': '删除成功'
        })


class TeacherCoursePublishView(APIView):
    """POST /api/teacher/courses/{id}/publish/ - 发布课程"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        # TODO: 实现课程发布
        return Response({
            'code': 200,
            'message': '发布成功',
            'data': {}
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
class TeacherChapterListView(APIView):
    """GET /api/teacher/courses/{courseId}/chapters/ - 获取章节列表"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, course_id):
        # TODO: 实现章节列表查询
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': {'chapters': []}
        })


class TeacherChapterCreateView(APIView):
    """POST /api/teacher/courses/{courseId}/chapters/ - 创建章节"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, course_id):
        # TODO: 实现章节创建
        return Response({
            'code': 200,
            'message': '创建成功',
            'data': {'chapter_id': None}
        }, status=status.HTTP_201_CREATED)


class TeacherChapterUpdateView(APIView):
    """PUT /api/teacher/courses/{courseId}/chapters/{id}/ - 更新章节"""
    permission_classes = [IsAuthenticated]
    
    def put(self, request, course_id, chapter_id):
        # TODO: 实现章节更新
        return Response({
            'code': 200,
            'message': '更新成功',
            'data': {}
        })


class TeacherChapterDeleteView(APIView):
    """DELETE /api/teacher/courses/{courseId}/chapters/{id}/ - 删除章节"""
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, course_id, chapter_id):
        # TODO: 实现章节删除
        return Response({
            'code': 200,
            'message': '删除成功'
        })


class TeacherChapterSortView(APIView):
    """POST /api/teacher/courses/{courseId}/chapters/sort/ - 排序章节"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, course_id):
        # TODO: 实现章节排序
        return Response({
            'code': 200,
            'message': '排序成功',
            'data': {}
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
class TeacherTermListView(APIView):
    """GET /api/teacher/courses/{courseId}/terms/ - 获取学期列表"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, course_id):
        # TODO: 实现学期列表查询
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': {'terms': []}
        })


class TeacherTermCreateView(APIView):
    """POST /api/teacher/courses/{courseId}/terms/ - 创建学期"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, course_id):
        # TODO: 实现学期创建
        return Response({
            'code': 200,
            'message': '创建成功',
            'data': {'term_id': None}
        }, status=status.HTTP_201_CREATED)


class TeacherTermUpdateView(APIView):
    """PUT /api/teacher/courses/{courseId}/terms/{id}/ - 更新学期"""
    permission_classes = [IsAuthenticated]
    
    def put(self, request, course_id, term_id):
        # TODO: 实现学期更新
        return Response({
            'code': 200,
            'message': '更新成功',
            'data': {}
        })


class TeacherTermDeleteView(APIView):
    """DELETE /api/teacher/courses/{courseId}/terms/{id}/ - 删除学期"""
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, course_id, term_id):
        # TODO: 实现学期删除
        return Response({
            'code': 200,
            'message': '删除成功'
        })


class TeacherClassListView(APIView):
    """GET /api/teacher/courses/{courseId}/classes/ - 获取班级列表"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, course_id):
        # TODO: 实现班级列表查询
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': {'classes': []}
        })


class TeacherClassCreateView(APIView):
    """POST /api/teacher/courses/{courseId}/classes/ - 创建班级"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, course_id):
        # TODO: 实现班级创建
        return Response({
            'code': 200,
            'message': '创建成功',
            'data': {'class_id': None}
        }, status=status.HTTP_201_CREATED)


class TeacherClassUpdateView(APIView):
    """PUT /api/teacher/courses/{courseId}/classes/{id}/ - 更新班级"""
    permission_classes = [IsAuthenticated]
    
    def put(self, request, course_id, class_id):
        # TODO: 实现班级更新
        return Response({
            'code': 200,
            'message': '更新成功',
            'data': {}
        })


class TeacherClassDeleteView(APIView):
    """DELETE /api/teacher/courses/{courseId}/classes/{id}/ - 删除班级"""
    permission_classes = [IsAuthenticated]
    
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
