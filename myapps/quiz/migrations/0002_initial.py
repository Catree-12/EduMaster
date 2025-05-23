# Generated by Django 5.1.6 on 2025-04-26 13:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('quiz', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='question_submission',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_submissions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='tiankong_answer',
            name='question',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='tiankong_answer', to='quiz.question'),
        ),
    ]
