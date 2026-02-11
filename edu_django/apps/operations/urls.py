# operations 应用的路由配置（管理员端）
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [
    # ===== 仪表板 =====
    # GET    /api/admin/dashboard/stats/ - 获取平台统计数据
    path('admin/dashboard/stats/', views.AdminDashboardStatsView.as_view(), name='admin-dashboard-stats'),
    
    # GET    /api/admin/dashboard/pending-tasks/ - 获取待处理任务
    path('admin/dashboard/pending-tasks/', views.AdminPendingTasksView.as_view(), name='admin-pending-tasks'),
    
    # ===== 课程审核 =====
    # GET    /api/admin/courses/pending/ - 获取待审核课程列表
    path('admin/courses/pending/', views.AdminPendingCoursesView.as_view(), name='admin-pending-courses'),
    
    # GET    /api/admin/courses/audit-list/ - 获取课程审核列表
    path('admin/courses/audit-list/', views.AdminCourseAuditListView.as_view(), name='admin-course-audit-list'),
    
    # GET    /api/admin/courses/{id}/audit-detail/ - 获取审核详情
    path('admin/courses/<int:pk>/audit-detail/', views.AdminCourseAuditDetailView.as_view(), name='admin-course-audit-detail'),
    
    # POST   /api/admin/courses/{id}/approve/ - 审核通过
    path('admin/courses/<int:pk>/approve/', views.AdminCourseApproveView.as_view(), name='admin-course-approve'),
    
    # POST   /api/admin/courses/{id}/reject/ - 审核拒绝
    path('admin/courses/<int:pk>/reject/', views.AdminCourseRejectView.as_view(), name='admin-course-reject'),
    
    # ===== 用户管理 =====
    # GET    /api/admin/users/ - 获取所有用户
    path('admin/users/', views.AdminUserListView.as_view(), name='admin-user-list'),
    
    # GET    /api/admin/users/{id}/ - 获取用户详情
    path('admin/users/<int:pk>/', views.AdminUserDetailView.as_view(), name='admin-user-detail'),
    
    # PUT    /api/admin/users/{id}/ - 更新用户信息
    path('admin/users/<int:pk>/', views.AdminUserUpdateView.as_view(), name='admin-user-update'),
    
    # POST   /api/admin/users/{id}/disable/ - 禁用用户
    path('admin/users/<int:pk>/disable/', views.AdminUserDisableView.as_view(), name='admin-user-disable'),
    
    # POST   /api/admin/users/{id}/enable/ - 启用用户
    path('admin/users/<int:pk>/enable/', views.AdminUserEnableView.as_view(), name='admin-user-enable'),
    
    # POST   /api/admin/users/batch-disable/ - 批量禁用
    path('admin/users/batch-disable/', views.AdminUserBatchDisableView.as_view(), name='admin-user-batch-disable'),
    
    # POST   /api/admin/users/batch-enable/ - 批量启用
    path('admin/users/batch-enable/', views.AdminUserBatchEnableView.as_view(), name='admin-user-batch-enable'),
    
    # REST API
    path('', include(router.urls)),
]

