# operations 应用的视图
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Create your views here.

# ==================== 仪表板 ====================
class AdminDashboardStatsView(APIView):
    """GET /api/admin/dashboard/stats/ - 获取平台统计数据"""
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response({'code': 200, 'message': '获取成功', 'data': {}})

class AdminPendingTasksView(APIView):
    """GET /api/admin/dashboard/pending-tasks/ - 获取待处理任务"""
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response({'code': 200, 'message': '获取成功', 'data': {'tasks': []}})

# ==================== 课程审核 ====================
class AdminPendingCoursesView(APIView):
    """GET /api/admin/courses/pending/ - 获取待审核课程列表"""
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response({'code': 200, 'message': '获取成功', 'data': {'results': []}})

class AdminCourseAuditListView(APIView):
    """GET /api/admin/courses/audit-list/ - 获取课程审核列表"""
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response({'code': 200, 'message': '获取成功', 'data': {'results': []}})

class AdminCourseAuditDetailView(APIView):
    """GET /api/admin/courses/{id}/audit-detail/ - 获取审核详情"""
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        return Response({'code': 200, 'message': '获取成功', 'data': {}})

class AdminCourseApproveView(APIView):
    """POST /api/admin/courses/{id}/approve/ - 审核通过"""
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        return Response({'code': 200, 'message': '审核通过', 'data': {}})

class AdminCourseRejectView(APIView):
    """POST /api/admin/courses/{id}/reject/ - 审核拒绝"""
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        return Response({'code': 200, 'message': '审核拒绝', 'data': {}})

# ==================== 用户管理 ====================
class AdminUserListView(APIView):
    """GET /api/admin/users/ - 获取所有用户"""
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response({'code': 200, 'message': '获取成功', 'data': {'results': []}})

class AdminUserDetailView(APIView):
    """GET /api/admin/users/{id}/ - 获取用户详情"""
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        return Response({'code': 200, 'message': '获取成功', 'data': {}})

class AdminUserUpdateView(APIView):
    """PUT /api/admin/users/{id}/ - 更新用户信息"""
    permission_classes = [IsAuthenticated]
    def put(self, request, pk):
        return Response({'code': 200, 'message': '更新成功', 'data': {}})

class AdminUserDisableView(APIView):
    """POST /api/admin/users/{id}/disable/ - 禁用用户"""
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        return Response({'code': 200, 'message': '禁用成功', 'data': {}})

class AdminUserEnableView(APIView):
    """POST /api/admin/users/{id}/enable/ - 启用用户"""
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        return Response({'code': 200, 'message': '启用成功', 'data': {}})

class AdminUserBatchDisableView(APIView):
    """POST /api/admin/users/batch-disable/ - 批量禁用"""
    permission_classes = [IsAuthenticated]
    def post(self, request):
        return Response({'code': 200, 'message': '批量禁用成功', 'data': {}})

class AdminUserBatchEnableView(APIView):
    """POST /api/admin/users/batch-enable/ - 批量启用"""
    permission_classes = [IsAuthenticated]
    def post(self, request):
        return Response({'code': 200, 'message': '批量启用成功', 'data': {}})
    pass


class AdminReportListView(APIView):
    """管理员内容审查(举报处理) - GET/POST"""
    pass
