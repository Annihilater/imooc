# Generated by Django 2.0 on 2019-03-19 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='category',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='课程类别'),
        ),
    ]
