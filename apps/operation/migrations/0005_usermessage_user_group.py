# Generated by Django 2.0 on 2019-03-22 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0004_remove_usermessage_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermessage',
            name='user_group',
            field=models.IntegerField(choices=[(1, '所有用户'), (2, '所有管理员'), (3, '单个用户')], default=3, verbose_name='接收信息的用户组'),
        ),
    ]
