# Generated by Django 2.0 on 2019-03-19 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_auto_20190319_1542'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='tag',
            field=models.CharField(default='', max_length=150, verbose_name='课程标签'),
        ),
    ]
