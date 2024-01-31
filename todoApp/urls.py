from . import views
from django.urls import path

urlpatterns = [
    path('register/',views.UserRegistration),
    path('verify-otp/',views.verifyOTP),
    path('login/',views.login),
    path('todo-groups/',views.todoGroup),
    path('tasks/',views.tasks),
    path('user-list/',views.user_list),
    path('overdue-tasks/',views.overdue_tasks),
    path('search-tasks/',views.search_tasks),
    path('update-task-status/',views.update_task_status),
    path('add-comment/',views.add_comments),
    path('assignee-mgmt/',views.assignee_mgmt),
    path('remove-assignee/',views.remove_assignee)
]
 