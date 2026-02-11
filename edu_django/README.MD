python manage.py runserver

python manage.py makemigrations

python manage.py migrate

python manage.py createsuperuser

python manage.py check：检查整个项目是否存在语法错误或配置问题，而不运行服务器。

1. 静态文件与测试
python manage.py collectstatic：部署上线前必用！它会将所有 App 下的图片、CSS、JS 收集到同一个目录下。

python manage.py test：运行你编写的测试用例，确保代码没被改出 Bug。