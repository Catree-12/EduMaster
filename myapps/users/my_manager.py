from django.contrib.auth.models import Group
from guardian.shortcuts import assign_perm
from .models import Studentuser, Teacheruser, Adminuser



    
    # def student_create(self,user,validated_data):
    #     student=Studentuser.objects.create(validated_data,user=user)
    #     return student
        
    # def teacher_create(self,user,validated_data):
    #     teacher=Teacheruser.objects.create(validated_data,user=user)
    #     return teacher
    
    # def admin_create(self,user,validated_data):
    #     admin=Adminuser.objects.create(user=user,validated_data=validated_data)
    #     return admin
        