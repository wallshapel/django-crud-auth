# Generated by Django 4.2.3 on 2023-08-08 13:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='userId',
            new_name='user',
        ),
    ]
