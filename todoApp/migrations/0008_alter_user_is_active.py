# Generated by Django 5.0.1 on 2024-01-30 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoApp', '0007_alter_user_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
