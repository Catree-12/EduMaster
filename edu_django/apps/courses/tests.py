from django.test import TestCase

# Create your tests here.
from django.db import migrations

def create_initial_categories(apps, schema_editor):
    CourseCategory = apps.get_model('courses', 'CourseCategory') # 替换 courses 为你的 app 名
    categories = [
        "计算机", "经济学", "农林园艺", "医药卫生", "理学", 
        "历史", "哲学", "法学", "文学文化", "艺术设计", 
        "外语", "教育教学", "管理学", "工学"
    ]
    for index, name in enumerate(categories):
        CourseCategory.objects.get_or_create(name=name, defaults={'order': index})

class Migration(migrations.Migration):
    dependencies = [
        ('courses', '0001_initial'), # 这里要填你上一个迁移文件的名字
    ]

    operations = [
        migrations.RunPython(create_initial_categories),
    ]