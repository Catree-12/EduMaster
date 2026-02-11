from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

# Create your views here.

# ==================== 公共社区 ====================
class PublicQuestionListView(APIView):
    """GET /api/community/questions/ - 获取社区问题列表"""
    permission_classes = [AllowAny]
    def get(self, request):
        return Response({'code': 200, 'message': '获取成功', 'data': {'results': []}})

class PublicQuestionDetailView(APIView):
    """GET /api/community/questions/{id}/ - 获取问题详情"""
    permission_classes = [AllowAny]
    def get(self, request, pk):
        return Response({'code': 200, 'message': '获取成功', 'data': {}})

class PostQuestionView(APIView):
    """POST /api/community/questions/ - 发布问题"""
    permission_classes = [IsAuthenticated]
    def post(self, request):
        return Response({'code': 200, 'message': '发布成功', 'data': {'question_id': None}}, status=status.HTTP_201_CREATED)

class UpdateQuestionView(APIView):
    """PUT /api/community/questions/{id}/ - 编辑问题"""
    permission_classes = [IsAuthenticated]
    def put(self, request, pk):
        return Response({'code': 200, 'message': '更新成功', 'data': {}})

class DeleteQuestionView(APIView):
    """DELETE /api/community/questions/{id}/ - 删除问题"""
    permission_classes = [IsAuthenticated]
    def delete(self, request, pk):
        return Response({'code': 200, 'message': '删除成功'})

class LikeQuestionView(APIView):
    """POST /api/community/questions/{id}/like/ - 点赞问题"""
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        return Response({'code': 200, 'message': '点赞成功', 'data': {}})

# ==================== 问答 ====================
class PostAnswerView(APIView):
    """POST /api/community/questions/{id}/answers/ - 回答问题"""
    permission_classes = [IsAuthenticated]
    def post(self, request, question_id):
        return Response({'code': 200, 'message': '回答成功', 'data': {'answer_id': None}}, status=status.HTTP_201_CREATED)

class UpdateAnswerView(APIView):
    """PUT /api/community/answers/{id}/ - 编辑回答"""
    permission_classes = [IsAuthenticated]
    def put(self, request, pk):
        return Response({'code': 200, 'message': '更新成功', 'data': {}})

class DeleteAnswerView(APIView):
    """DELETE /api/community/answers/{id}/ - 删除回答"""
    permission_classes = [IsAuthenticated]
    def delete(self, request, pk):
        return Response({'code': 200, 'message': '删除成功'})

class LikeAnswerView(APIView):
    """POST /api/community/answers/{id}/like/ - 点赞回答"""
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        return Response({'code': 200, 'message': '点赞成功', 'data': {}})

# ==================== 课程社区（学生） ====================
class StudentThreadListView(APIView):
    """GET /api/student/courses/{courseId}/threads/ - 获取课程话题列表"""
    permission_classes = [IsAuthenticated]
    def get(self, request, course_id):
        return Response({'code': 200, 'message': '获取成功', 'data': {'threads': []}})

class StudentThreadDetailView(APIView):
    """GET /api/student/courses/{courseId}/threads/{threadId}/ - 获取话题详情"""
    permission_classes = [IsAuthenticated]
    def get(self, request, course_id, thread_id):
        return Response({'code': 200, 'message': '获取成功', 'data': {}})

class StudentThreadCreateView(APIView):
    """POST /api/student/courses/{courseId}/threads/ - 发布话题"""
    permission_classes = [IsAuthenticated]
    def post(self, request, course_id):
        return Response({'code': 200, 'message': '发布成功', 'data': {'thread_id': None}}, status=status.HTTP_201_CREATED)

class StudentThreadUpdateView(APIView):
    """PUT /api/student/courses/{courseId}/threads/{threadId}/ - 编辑话题"""
    permission_classes = [IsAuthenticated]
    def put(self, request, course_id, thread_id):
        return Response({'code': 200, 'message': '更新成功', 'data': {}})

class StudentThreadDeleteView(APIView):
    """DELETE /api/student/courses/{courseId}/threads/{threadId}/ - 删除话题"""
    permission_classes = [IsAuthenticated]
    def delete(self, request, course_id, thread_id):
        return Response({'code': 200, 'message': '删除成功'})

class StudentThreadCommentView(APIView):
    """POST /api/student/courses/{courseId}/threads/{threadId}/comments/ - 发布评论"""
    permission_classes = [IsAuthenticated]
    def post(self, request, course_id, thread_id):
        return Response({'code': 200, 'message': '发布成功', 'data': {'comment_id': None}}, status=status.HTTP_201_CREATED)

# ==================== 课程社区（教师） ====================
class TeacherThreadListView(APIView):
    """GET /api/teacher/courses/{courseId}/threads/ - 获取课程话题列表"""
    permission_classes = [IsAuthenticated]
    def get(self, request, course_id):
        return Response({'code': 200, 'message': '获取成功', 'data': {'threads': []}})

class TeacherThreadDetailView(APIView):
    """GET /api/teacher/courses/{courseId}/threads/{threadId}/ - 获取话题详情"""
    permission_classes = [IsAuthenticated]
    def get(self, request, course_id, thread_id):
        return Response({'code': 200, 'message': '获取成功', 'data': {}})

class TeacherThreadCreateView(APIView):
    """POST /api/teacher/courses/{courseId}/threads/ - 发布公告/话题"""
    permission_classes = [IsAuthenticated]
    def post(self, request, course_id):
        return Response({'code': 200, 'message': '发布成功', 'data': {'thread_id': None}}, status=status.HTTP_201_CREATED)

class TeacherThreadUpdateView(APIView):
    """PUT /api/teacher/courses/{courseId}/threads/{threadId}/ - 编辑话题"""
    permission_classes = [IsAuthenticated]
    def put(self, request, course_id, thread_id):
        return Response({'code': 200, 'message': '更新成功', 'data': {}})

class TeacherThreadDeleteView(APIView):
    """DELETE /api/teacher/courses/{courseId}/threads/{threadId}/ - 删除话题"""
    permission_classes = [IsAuthenticated]
    def delete(self, request, course_id, thread_id):
        return Response({'code': 200, 'message': '删除成功'})

class PinThreadView(APIView):
    """POST /api/teacher/courses/{courseId}/threads/{threadId}/pin/ - 置顶话题"""
    permission_classes = [IsAuthenticated]
    def post(self, request, course_id, thread_id):
        return Response({'code': 200, 'message': '置顶成功', 'data': {}})

class UnpinThreadView(APIView):
    """POST /api/teacher/courses/{courseId}/threads/{threadId}/unpin/ - 取消置顶"""
    permission_classes = [IsAuthenticated]
    def post(self, request, course_id, thread_id):
        return Response({'code': 200, 'message': '取消置顶成功', 'data': {}})

