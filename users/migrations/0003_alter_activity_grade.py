# Generated by Django 3.2.2 on 2021-05-11 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_rename_user_id_activity_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='grade',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
    ]