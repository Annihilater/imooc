# Generated by Django 2.0 on 2019-03-23 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0003_teacher_age'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseorg',
            name='tag',
            field=models.CharField(default='全国知名', max_length=10, verbose_name='机构标签'),
        ),
    ]
