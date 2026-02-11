# exams 应用的视图
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Create your views here.

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


# ==================== 教师考试管理 ====================
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
