# Generated by Django 5.0 on 2024-01-29 05:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=8)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Tasks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('due_date', models.DateField(null=True)),
                ('comments', models.CharField(max_length=200)),
                ('files', models.FileField(blank=True, null=True, upload_to='taskfiles/')),
                ('completion_status', models.CharField(choices=[('Incomplete', 'Incomplete'), ('Completed', 'Completed')], default='Incomplete', max_length=20)),
                ('assignee', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TodoGroups',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_name', models.CharField(max_length=200)),
                ('group_description', models.TextField()),
                ('tasks', models.ManyToManyField(to='todoApp.tasks')),
                ('users', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='todo_groups', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
