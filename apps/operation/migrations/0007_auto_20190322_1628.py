# Generated by Django 2.0 on 2019-03-22 16:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0006_auto_20190322_1611'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usermessage',
            old_name='user_id',
            new_name='user',
        ),
    ]