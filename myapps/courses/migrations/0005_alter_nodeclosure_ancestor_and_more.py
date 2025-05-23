# Generated by Django 5.1.6 on 2025-05-17 16:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_alter_section_content_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nodeclosure',
            name='ancestor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='descendant_relations', to='courses.node'),
        ),
        migrations.AlterField(
            model_name='nodeclosure',
            name='descendant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ancestor_relations', to='courses.node'),
        ),
    ]
