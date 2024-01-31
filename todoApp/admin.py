from django.contrib import admin
from .models import User, TodoGroups, Tasks,Comments


class CommentAdmin(admin.ModelAdmin):
    list_display=['user','task','comment']


class UserAdmin(admin.ModelAdmin):
    list_display=['username','email','is_verified']


class TodoGroupAdmin(admin.ModelAdmin):
    list_display=['group_name','user']

class TasksAdmin(admin.ModelAdmin):
    list_display=['title','created_by','completion_status','todo_group']

admin.site.register(User,UserAdmin)

admin.site.register(Tasks,TasksAdmin)
admin.site.register(TodoGroups,TodoGroupAdmin)
admin.site.register(Comments,CommentAdmin)