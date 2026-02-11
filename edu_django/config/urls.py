"""
URL configuration for edu_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger配置
schema_view = get_schema_view(
    openapi.Info(
        title="EduMaster API",
        default_version='v1',
        description="在线教育平台API文档 - 基于 Django 5.1",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API文档
    path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # 业务应用路由 (统一使用 /api/ 前缀)
    # 认证模块 (users app)
    path('api/', include('users.urls')),  # 包含 /api/auth/* 路由
    
    # 课程模块 (courses app) - 包含教师端、学生端、公共端
    path('api/', include('courses.urls')),  #  courses/*
    
    # 学习模块 (learning app) - 选课与证书
    path('api/', include('learning.urls')),  
    
    # 作业模块 (homework app)
    path('api/', include('homework.urls')),  # teacher/homework/*, student/homework/*
    
    # 考试模块 (exams app)
    path('api/', include('exams.urls')),  # teacher/exams/*, student/exams/*
    
    # 管理员模块 (operations app)
    path('api/', include('operations.urls')),  # admin/dashboard/*, admin/users/*, admin/courses/audit-list/*
    
    # 知识图谱模块 (knowledge app)
    path('api/knowledge/', include('knowledge.urls')),
    
    # 社区模块 (community app)
    path('api/community/', include('community.urls')),
    
    # 财务模块 (finance app)
    path('api/finance/', include('finance.urls')),
    
    # 系统模块 (system app)
    path('api/system/', include('system.urls')),
]

# 开发环境下提供媒体文件访问
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
