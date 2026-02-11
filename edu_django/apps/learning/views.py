# learning 应用的视图
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.

class StudentEnrollmentListView(APIView):
    """学生选课列表 - GET获取我的选课, POST选课/报名"""
    pass


class StudentCertificateListView(APIView):
    """学生证书列表 - GET获取我的证书"""
    pass
