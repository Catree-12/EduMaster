# users 应用的视图
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.core.cache import cache
from django.utils import timezone
from django.http import FileResponse
from .models import User, StudentProfile, TeacherProfile
import random
import re

# Create your views here.

class LoginView(APIView):
    """用户登录 - JWT认证"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        """
        登录接口
        参数: email, password
        返回: access_token, refresh_token, user_info
        """
        email = request.data.get('email', '').strip()
        password = request.data.get('password')
        
        if not email or not password:
            return Response({
                'code': 400,
                'message': '邮箱和密码不能为空'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 通过邮箱登录
        user = authenticate(username=email, password=password)
        
        if user is None:
            return Response({
                'code': 401,
                'message': '邮箱或密码错误'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        if not user.is_active:
            return Response({
                'code': 403,
                'message': '账户已被禁用'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # 生成JWT令牌
        refresh = RefreshToken.for_user(user)
        
        # 获取用户身份信息（每个用户都有学生和教师身份）
        student_id = user.student_profile.student_id if hasattr(user, 'student_profile') else None
        teacher_id = user.teacher_profile.teacher_id if hasattr(user, 'teacher_profile') else None
        
        return Response({
            'code': 200,
            'message': '登录成功',
            'data': {
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
                'user': {
                    'id': user.id,
                    'real_name': user.real_name,
                    'nickname': user.nickname,
                    'email': user.email,
                    'phone': user.phone,
                    'avatar': user.avatar.url if user.avatar else None,
                    'is_admin': user.is_superuser,
                    'gender': user.gender,
                    'school': user.school,
                    'major': user.major,
                    'student_id': student_id,
                    'teacher_id': teacher_id
                }
            }
        })


class RegisterView(APIView):
    """用户注册"""
    permission_classes = [AllowAny]
    authentication_classes = []
    
    def post(self, request):
        """
        注册接口
        参数: real_name (真实姓名), email, password
        """
        # 1. 获取数据并去空格
        real_name = request.data.get('real_name', '').strip() 
        email = request.data.get('email', '').strip()
        password = request.data.get('password')
        
        # 2. 验证必填字段
        if not all([real_name, email, password]):
            return Response({
                'code': 400,
                'message': '真实姓名、邮箱和密码不能为空'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 3. 检查邮箱是否已存在
        if User.objects.filter(email=email).exists():
            return Response({
                'code': 400,
                'message': '该邮箱已被注册'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 4. 创建用户
            user = User.objects.create_user(
                username=email,        # 数据库的唯一标识用邮箱填
                email=email,           # 登录用邮箱
                password=password,
                real_name=real_name,   # 真实姓名（允许重复）
                nickname=real_name     # 初始网名默认也用真实姓名
            )
            
            # 5. 同时创建学生和教师两个身份
            year = timezone.now().strftime('%Y')
            max_attempts = 10  # 最多尝试10次生成唯一ID
            
            # 5.1 创建学生身份（S开头）
            student_id = None
            for _ in range(max_attempts):
                # 生成年份 + 6位随机数
                random_num = ''.join([str(random.randint(0, 9)) for _ in range(6)])
                student_id = f"S{year}{random_num}"
                
                # 检查是否已存在
                if not StudentProfile.objects.filter(student_id=student_id).exists():
                    StudentProfile.objects.create(user=user, student_id=student_id)
                    break
            else:
                # 如果10次都失败，使用用户ID作为后备方案
                student_id = f"S{year}{user.id:06d}"
                StudentProfile.objects.create(user=user, student_id=student_id)
            
            # 5.2 创建教师身份（T开头）
            teacher_id = None
            for _ in range(max_attempts):
                # 生成年份 + 6位随机数
                random_num = ''.join([str(random.randint(0, 9)) for _ in range(6)])
                teacher_id = f"T{year}{random_num}"
                
                # 检查是否已存在
                if not TeacherProfile.objects.filter(teacher_id=teacher_id).exists():
                    TeacherProfile.objects.create(user=user, teacher_id=teacher_id)
                    break
            else:
                # 如果10次都失败，使用用户ID作为后备方案
                teacher_id = f"T{year}{user.id:06d}"
                TeacherProfile.objects.create(user=user, teacher_id=teacher_id)
            
            return Response({
                'code': 200,
                'message': '注册成功',
                'data': {
                    'user_id': user.id,
                    'real_name': user.real_name,
                    'email': user.email,
                    'student_id': student_id,
                    'teacher_id': teacher_id
                }
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                'code': 500,
                'message': f'注册失败: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LogoutView(APIView):
    """用户登出"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        登出接口 - 将refresh_token加入黑名单
        参数: refresh_token
        """
        try:
            refresh_token = request.data.get('refresh_token')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            
            return Response({
                'code': 200,
                'message': '登出成功'
            })
        except Exception as e:
            return Response({
                'code': 400,
                'message': f'登出失败: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)


class ForgetPasswordView(APIView):
    """忘记密码"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        """
        忘记密码 - 发送验证码
        参数: phone
        """
        phone = request.data.get('phone')
        
        if not phone:
            return Response({
                'code': 400,
                'message': '手机号不能为空'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 检查手机号是否存在
        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            return Response({
                'code': 404,
                'message': '该手机号未注册'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # 生成6位验证码
        code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        
        # 将验证码存入缓存，有效期5分钟
        cache_key = f'reset_pwd_code_{phone}'
        cache.set(cache_key, code, 300)
        
        # TODO: 调用短信服务发送验证码
        # send_sms(phone, code)
        
        return Response({
            'code': 200,
            'message': '验证码已发送',
            'data': {
                'code': code  # 开发环境返回验证码，生产环境删除此行
            }
        })
    
    def put(self, request):
        """
        重置密码
        参数: phone, code, new_password
        """
        phone = request.data.get('phone')
        code = request.data.get('code')
        new_password = request.data.get('new_password')
        
        if not all([phone, code, new_password]):
            return Response({
                'code': 400,
                'message': '手机号、验证码和新密码不能为空'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 验证验证码
        cache_key = f'reset_pwd_code_{phone}'
        cached_code = cache.get(cache_key)
        
        if not cached_code:
            return Response({
                'code': 400,
                'message': '验证码已过期'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if cached_code != code:
            return Response({
                'code': 400,
                'message': '验证码错误'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 重置密码
        try:
            user = User.objects.get(phone=phone)
            user.set_password(new_password)
            user.save()
            
            # 删除验证码
            cache.delete(cache_key)
            
            return Response({
                'code': 200,
                'message': '密码重置成功'
            })
        except User.DoesNotExist:
            return Response({
                'code': 404,
                'message': '用户不存在'
            }, status=status.HTTP_404_NOT_FOUND)


class ChangePasswordView(APIView):
    """修改密码 - 需要登录"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        修改密码
        参数: old_password, new_password
        """
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        # 获取前端传来的 refresh_token
        refresh_token = request.data.get('refresh_token')
        # 1. 验证必填
        if not all([old_password, new_password]):
            return Response({
                'code': 400,
                'message': '旧密码和新密码不能为空'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 2. 【新增】验证新旧密码是否相同
        if old_password == new_password:
            return Response({
                'code': 400,
                'message': '新密码不能与旧密码相同'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 3. 验证旧密码（数据库匹配）
        if not user.check_password(old_password):
            return Response({
                'code': 400,
                'message': '旧密码错误'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 4. 设置新密码
        # set_password 会自动帮你把明文密码进行哈希（Hash）加密存储
        user.set_password(new_password)
        user.save()
        # 2. 如果传了 refresh，将其加入黑名单
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist() # 核心代码：强制失效
            except Exception:
                pass # token 可能已经过期或无效，忽略
            
        return Response({
            'code': 200,
            'message': '密码修改成功，请重新登录'
        })

class RefreshTokenView(APIView):
    """刷新Token - 需要登录"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        """
        刷新Token
        参数: refresh_token
        """
        refresh_token = request.data.get('refresh_token')
        
        if not refresh_token:
            return Response({
                'code': 400,
                'message': 'refresh_token不能为空'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            token = RefreshToken(refresh_token)
            new_access_token = str(token.access_token)
            
            return Response({
                'code': 200,
                'message': 'Token刷新成功',
                'data': {
                    'access_token': new_access_token
                }
            })
        except Exception as e:
            return Response({
                'code': 400,
                'message': f'Token刷新失败: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)
        

class ProfileView(APIView):
    """获取/更新个人信息"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """获取个人信息"""
        user = request.user
        
        # 获取用户身份信息（每个用户都有学生和教师身份）
        student_id = user.student_profile.student_id if hasattr(user, 'student_profile') else None
        teacher_id = user.teacher_profile.teacher_id if hasattr(user, 'teacher_profile') else None
        
        data = {
            # 'id': user.id,
            'email': user.email,
            'real_name': user.real_name,
            'nickname': user.nickname,
            'phone': user.phone,
            'avatar': user.avatar.url if user.avatar else None,
            'bio': user.bio,
            'gender': user.gender,
            'school': user.school,
            'major': user.major,
            # 'is_admin': user.is_superuser,
            'student_id': student_id,
            'teacher_id': teacher_id,
            'created_at': user.created_at.strftime('%Y-%m-%d'),
            # 'updated_at': user.updated_at.isoformat()
        }
        
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': data
        })
    
    def put(self, request):
        """更新个人信息"""
        user = request.user
        
        # 可更新的字段
        updatable_fields = ['real_name', 'nickname', 'bio', 'gender', 'school', 'major', 'phone']
        
        for field in updatable_fields:
            if field in request.data:
                setattr(user, field, request.data[field])
        
        # 处理头像上传
        if 'avatar' in request.FILES:
            user.avatar = request.FILES['avatar']
        
        user.save()
        
        return Response({
            'code': 200,
            'message': '更新成功',
            'data': {
            'email': user.email,
            'real_name': user.real_name,
            'nickname': user.nickname,
            'phone': user.phone,
            'avatar': user.avatar.url if user.avatar else None,
            'bio': user.bio,
            'gender': user.gender,
            'school': user.school,
            'major': user.major,
        }
        })


# class CurrentUserView(APIView):
#     """GET /api/users/me/ - 获取当前登录用户基本信息"""
#     permission_classes = [IsAuthenticated]
    
#     def get(self, request):
#         user = request.user
        
#         # 获取用户身份信息（每个用户都有学生和教师身份）
#         student_id = user.student_profile.student_id if hasattr(user, 'student_profile') else None
#         teacher_id = user.teacher_profile.teacher_id if hasattr(user, 'teacher_profile') else None
        
#         return Response({
#             'code': 200,
#             'message': '获取成功',
#             'data': {
#                 'id': user.id,
#                 'email': user.email,
#                 'real_name': user.real_name,
#                 'nickname': user.nickname,
#                 'avatar': user.avatar.url if user.avatar else None,
#                 'is_admin': user.is_superuser,
#                 'student_id': student_id,
#                 'teacher_id': teacher_id
#             }
#         })
    
class UserDetailView(APIView):
    """GET /api/users/{id}/ - 获取指定用户详情"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        try:
            user = User.objects.get(id=pk)
            
            # 获取用户身份信息（每个用户都有学生和教师身份）
            student_id = user.student_profile.student_id if hasattr(user, 'student_profile') else None
            teacher_id = user.teacher_profile.teacher_id if hasattr(user, 'teacher_profile') else None
            
            data = {
                'id': user.id,
                'email': user.email,
                'real_name': user.real_name,
                'nickname': user.nickname,
                'avatar': user.avatar.url if user.avatar else None,
                'bio': user.bio,
                'is_admin': user.is_superuser,
                'student_id': student_id,
                'teacher_id': teacher_id,
                'created_at': user.created_at.isoformat()
            }
            
            return Response({'code': 200, 'message': '获取成功', 'data': data})
        except User.DoesNotExist:
            return Response({
                'code': 404,
                'message': '用户不存在'
            }, status=status.HTTP_404_NOT_FOUND)


class AvatarUploadView(APIView):
    """POST /api/users/avatar/ - 上传头像"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user
        
        if 'avatar' not in request.FILES:
            return Response({
                'code': 400,
                'message': '请上传头像文件'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user.avatar = request.FILES['avatar']
        user.save()
        
        return Response({
            'code': 200,
            'message': '上传成功',
            'data': {
                'avatar': user.avatar.url
            }
        })


class LearningStatsView(APIView):
    """GET /api/users/stats/learning/ - 获取学习统计"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # TODO: 实现学习统计逻辑
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': {
                'total_courses': 0,
                'completed_courses': 0,
                'ongoing_courses': 0,
                'learning_hours': 0
            }
        })


class GradeStatsView(APIView):
    """GET /api/users/stats/grades/ - 获取成绩统计"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # TODO: 实现成绩统计逻辑
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': {
                'average_grade': 0,
                'highest_grade': 0,
                'lowest_grade': 0,
                'total_exams': 0
            }
        })


class CertificateStatsView(APIView):
    """GET /api/users/stats/certificates/ - 获取证书统计"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # TODO: 实现证书统计逻辑
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': {
                'total_certificates': 0,
                'course_certificates': 0,
                'skill_certificates': 0
            }
        })


class CertificateListView(APIView):
    """GET /api/users/certificates/ - 获取证书列表"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # TODO: 实现证书列表查询
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': {
                'results': [],
                'count': 0,
                'next': None,
                'previous': None,
                'page': 1,
                'pageSize': 10,
                'totalPages': 0
            }
        })


class CertificateDetailView(APIView):
    """GET /api/users/certificates/{id}/ - 获取证书详情"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        # TODO: 实现证书详情查询
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': {}
        })


class CertificateShareView(APIView):
    """POST /api/users/certificates/{id}/share/ - 生成证书分享链接"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        # TODO: 实现证书分享链接生成
        return Response({
            'code': 200,
            'message': '分享链接已生成',
            'data': {
                'share_url': '',
                'share_code': '',
                'expiry_date': None
            }
        })


class CertificateDownloadView(APIView):
    """GET /api/users/certificates/{id}/download/ - 下载证书文件"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        # TODO: 实现证书下载
        return Response({
            'code': 200,
            'message': '下载成功'
        })


class GenerateCourseCertificateView(APIView):
    """POST /api/users/courses/{courseId}/certificate/ - 生成课程证书"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, course_id):
        # TODO: 实现课程证书生成
        return Response({
            'code': 200,
            'message': '证书已生成',
            'data': {
                'certificate_id': None
            }
        })


class MessageListView(APIView):
    """GET /api/users/messages/ - 获取消息列表"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # TODO: 实现消息列表查询
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': {
                'results': [],
                'count': 0,
                'next': None,
                'previous': None,
                'page': 1,
                'pageSize': 10,
                'totalPages': 0
            }
        })


class MarkMessageReadView(APIView):
    """POST /api/users/messages/{id}/read/ - 标记消息已读"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        # TODO: 实现消息标记已读
        return Response({
            'code': 200,
            'message': '标记成功'
        })
