# Generated by Django 3.2.2 on 2021-05-11 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_activity_grade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='repo',
            field=models.CharField(max_length=255),
        ),
    ]
