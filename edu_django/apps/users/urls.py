# users 应用的路由配置
from django.urls import path
from . import views

urlpatterns = [
    # ===== 认证模块 (Authentication) =====
    # POST   /api/auth/login/
    path('auth/login/', views.LoginView.as_view(), name='auth-login'),
    
    # POST   /api/auth/register/
    path('auth/register/', views.RegisterView.as_view(), name='auth-register'),
    
    # POST   /api/auth/logout/
    path('auth/logout/', views.LogoutView.as_view(), name='auth-logout'),
    
    # POST   /api/auth/forget-password/  (发送验证码)
    # PUT    /api/auth/forget-password/  (重置密码)
    path('auth/forget-password/', views.ForgetPasswordView.as_view(), name='auth-forget-password'),
    
    # POST   /api/auth/change-password/
    path('auth/change-password/', views.ChangePasswordView.as_view(), name='auth-change-password'),

    # POST   /api/auth/refresh/ - 刷新Token
    path('auth/refresh/', views.RefreshTokenView.as_view(), name='auth-refresh'),
    
    # ===== 用户模块 (Users) =====
    # GET    /api/users/me/ - 获取当前登录用户基本信息
    # path('users/me/', views.CurrentUserView.as_view(), name='users-me'),
    
    # GET    /api/users/{id}/ - 获取指定用户详情
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
    
    # GET    /api/users/profile/ - 获取当前用户完整信息（含 profile）
    # PUT    /api/users/profile/ - 更新用户信息
    path('users/profile/', views.ProfileView.as_view(), name='user-profile'),
    
    # POST   /api/users/avatar/ - 上传头像
    path('users/avatar/', views.AvatarUploadView.as_view(), name='user-avatar'),
    
    # GET    /api/users/stats/learning/ - 获取学习统计
    path('users/stats/learning/', views.LearningStatsView.as_view(), name='user-learning-stats'),
    
    # GET    /api/users/stats/grades/ - 获取成绩统计
    path('users/stats/grades/', views.GradeStatsView.as_view(), name='user-grade-stats'),
    
    # GET    /api/users/stats/certificates/ - 获取证书统计
    path('users/stats/certificates/', views.CertificateStatsView.as_view(), name='user-certificate-stats'),
    
    # GET    /api/users/certificates/ - 获取证书列表
    path('users/certificates/', views.CertificateListView.as_view(), name='user-certificates'),
    
    # GET    /api/users/certificates/{id}/ - 获取证书详情
    path('users/certificates/<int:pk>/', views.CertificateDetailView.as_view(), name='user-certificate-detail'),
    
    # POST   /api/users/certificates/{id}/share/ - 生成证书分享链接
    path('users/certificates/<int:pk>/share/', views.CertificateShareView.as_view(), name='user-certificate-share'),
    
    # GET    /api/users/certificates/{id}/download/ - 下载证书文件
    path('users/certificates/<int:pk>/download/', views.CertificateDownloadView.as_view(), name='user-certificate-download'),
    
    # POST   /api/users/courses/{courseId}/certificate/ - 生成课程证书
    path('users/courses/<int:course_id>/certificate/', views.GenerateCourseCertificateView.as_view(), name='generate-course-certificate'),
    
    # GET    /api/users/messages/ - 获取消息列表
    path('users/messages/', views.MessageListView.as_view(), name='user-messages'),
    
    # POST   /api/users/messages/{id}/read/ - 标记消息已读
    path('users/messages/<int:pk>/read/', views.MarkMessageReadView.as_view(), name='mark-message-read'),
]
