# # edumaster/signals.py
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.contrib.auth.models import Group, Permission
# from guardian.shortcuts import assign_perm
# from .models import User, Studentuser, Teacheruser, Adminuser
# from django.contrib.contenttypes.models import ContentType


# # 初始化组和权限（在首次迁移后运行）
# def create_groups_and_permissions(sender, **kwargs):

#     student_content_type = ContentType.objects.get_for_model(Studentuser)
#     teacher_content_type = ContentType.objects.get_for_model(Teacheruser)
#     admin_content_type = ContentType.objects.get_for_model(Adminuser)
#     # 公共权限组（所有用户）
#     base_group, created = Group.objects.get_or_create(name='base_group')
#     assign_perm('usersview_user', base_group)
   

#     # 学生组
#     student_group, created = Group.objects.get_or_create(name='student_group')

#     # student_perms = [
#     #     'enroll_course',     # 选课
#     #     'submit_homework',   # 提交作业
#     #     'view_grade',        # 查看成绩（假设 Grade 模型有 view_grade 权限）
#     # ]


#     # 教师组
#     teacher_group, created = Group.objects.get_or_create(name='teacher_group')

#     # teacher_perms = [
#     #     'add_course',        # 创建课程
#     #     'grade_homework',    # 批改作业
#     # ]

# # 注册信号
# from django.core.signals import post_migrate
# post_migrate.connect(create_groups_and_permissions)

# # # 用户注册时分配权限
# # @receiver(post_save, sender=User)
# # def handle_user_creation(sender, instance, created, **kwargs):
# #     if created:
# #         # 分配公共组
# #         base_group = Group.objects.get(name='base_group')
# #         instance.groups.add(base_group)
        
# #         # 根据角色分配组
# #         if instance.role == 'student':
# #             student_group = Group.objects.get(name='student_group')
            
# #             instance.groups.add(student_group)
# #         elif instance.role == 'teacher':
# #             teacher_group = Group.objects.get(name='teacher_group')
# #             instance.groups.add(teacher_group)
# #         elif instance.role == 'admin':
# #             instance.is_staff = True
# #             instance.save()

# #         # 关键步骤：分配对象级权限（使用 guardian）
# #         # 允许用户修改自己的账户
# #         assign_perm('auth.change_user', instance, instance)
# #         assign_perm('auth.view_user', instance, instance)
# # edumaster/signals.py
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.contrib.auth.models import Group, Permission
# from guardian.shortcuts import assign_perm
# from .models import User, Studentuser, Teacheruser, Adminuser
# from django.contrib.contenttypes.models import ContentType


# # 初始化组和权限（在首次迁移后运行）
# def create_groups_and_permissions(sender, **kwargs):

#     student_content_type = ContentType.objects.get_for_model(Studentuser)
#     teacher_content_type = ContentType.objects.get_for_model(Teacheruser)
#     admin_content_type = ContentType.objects.get_for_model(Adminuser)
#     # 公共权限组（所有用户）
#     base_group, created = Group.objects.get_or_create(name='base_group')
#     assign_perm('usersview_user', base_group)
   

#     # 学生组
#     student_group, created = Group.objects.get_or_create(name='student_group')

#     # student_perms = [
#     #     'enroll_course',     # 选课
#     #     'submit_homework',   # 提交作业
#     #     'view_grade',        # 查看成绩（假设 Grade 模型有 view_grade 权限）
#     # ]


#     # 教师组
#     teacher_group, created = Group.objects.get_or_create(name='teacher_group')

#     # teacher_perms = [
#     #     'add_course',        # 创建课程
#     #     'grade_homework',    # 批改作业
#     # ]

# # 注册信号
# from django.core.signals import post_migrate
# post_migrate.connect(create_groups_and_permissions)

# # # 用户注册时分配权限
# # @receiver(post_save, sender=User)
# # def handle_user_creation(sender, instance, created, **kwargs):
# #     if created:
# #         # 分配公共组
# #         base_group = Group.objects.get(name='base_group')
# #         instance.groups.add(base_group)
        
# #         # 根据角色分配组
# #         if instance.role == 'student':
# #             student_group = Group.objects.get(name='student_group')
            
# #             instance.groups.add(student_group)
# #         elif instance.role == 'teacher':
# #             teacher_group = Group.objects.get(name='teacher_group')
# #             instance.groups.add(teacher_group)
# #         elif instance.role == 'admin':
# #             instance.is_staff = True
# #             instance.save()

# #         # 关键步骤：分配对象级权限（使用 guardian）
# #         # 允许用户修改自己的账户
# #         assign_perm('auth.change_user', instance, instance)
# #         assign_perm('auth.view_user', instance, instance)
