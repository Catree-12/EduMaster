# homework 应用的视图
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Create your views here.

# ==================== 学生作业 ====================
class StudentHomeworkListView(APIView):
    """GET /api/student/homework/ - 获取作业列表"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # TODO: 实现作业列表查询
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': {'results': []}
        })


class StudentHomeworkDetailView(APIView):
    """GET /api/student/courses/{courseId}/homework/{homeworkId}/ - 获取作业详情"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, course_id, homework_id):
        # TODO: 实现作业详情查询
        return Response({'code': 200, 'message': '获取成功', 'data': {}})


class StudentHomeworkSubmitView(APIView):
    """POST /api/student/courses/{courseId}/homework/{homeworkId}/submit/ - 提交作业"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, course_id, homework_id):
        # TODO: 实现作业提交（NLP/Rule-Based预判分）
        return Response({
            'code': 200,
            'message': '提交成功',
            'data': {'submission_id': None}
        }, status=status.HTTP_201_CREATED)


class StudentHomeworkSubmissionView(APIView):
    """GET /api/student/courses/{courseId}/homework/{homeworkId}/submission/ - 获取作业提交详情"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, course_id, homework_id):
        # TODO: 实现提交详情查询
        return Response({'code': 200, 'message': '获取成功', 'data': {}})


# ==================== 教师作业管理 ====================
class TeacherHomeworkListView(APIView):
    """GET /api/teacher/homework/ - 获取作业库"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # TODO: 实现作业库列表查询
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': {'results': []}
        })


class TeacherHomeworkDetailView(APIView):
    """GET /api/teacher/homework/{id}/ - 获取作业详情"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        # TODO: 实现作业详情查询
        return Response({'code': 200, 'message': '获取成功', 'data': {}})


class TeacherHomeworkCreateView(APIView):
    """POST /api/teacher/homework/ - 创建作业"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # TODO: 实现作业创建
        return Response({
            'code': 200,
            'message': '创建成功',
            'data': {'homework_id': None}
        }, status=status.HTTP_201_CREATED)


class TeacherHomeworkUpdateView(APIView):
    """PUT /api/teacher/homework/{id}/ - 更新作业"""
    permission_classes = [IsAuthenticated]
    
    def put(self, request, pk):
        # TODO: 实现作业更新
        return Response({
            'code': 200,
            'message': '更新成功',
            'data': {}
        })


class TeacherHomeworkDeleteView(APIView):
    """DELETE /api/teacher/homework/{id}/ - 删除作业"""
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, pk):
        # TODO: 实现作业删除
        return Response({
            'code': 200,
            'message': '删除成功'
        })


class TeacherHomeworkPublishView(APIView):
    """POST /api/teacher/homework/{id}/publish/ - 发布作业"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        # TODO: 实现作业发布
        return Response({
            'code': 200,
            'message': '发布成功',
            'data': {}
        })


class TeacherHomeworkSubmissionsView(APIView):
    """GET /api/teacher/homework/{id}/submissions/ - 获取作业提交列表"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        # TODO: 实现提交列表查询
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': {'results': []}
        })


class TeacherHomeworkGradeView(APIView):
    """POST /api/teacher/homework/{homework_id}/submissions/{submission_id}/grade/ - 批改作业"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, homework_id, submission_id):
        # TODO: 实现作业批改（Auto-Grading支持）
        return Response({
            'code': 200,
            'message': '批改成功',
            'data': {}
        })
