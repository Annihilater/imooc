# Generated by Django 2.0 on 2019-03-19 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_course_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='category',
            field=models.CharField(blank=True, default='后端开发', max_length=20, null=True, verbose_name='课程类别'),
        ),
    ]
