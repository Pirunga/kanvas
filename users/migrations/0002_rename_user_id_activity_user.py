# Generated by Django 3.2.2 on 2021-05-11 17:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='activity',
            old_name='user_id',
            new_name='user',
        ),
    ]