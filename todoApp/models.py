from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from todoApp.managers import UserManager

class User(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=300)
    is_verified=models.BooleanField(default=False)
    otp=models.IntegerField(blank=True,null=True)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password']
    objects=UserManager()
    
    def __str__(self):
        return self.email
    
    def has_module_perms(self, app_label):
        return self.is_staff

    def has_perm(self, perm, obj=None):
        return self.is_staff
    
class TodoGroups(models.Model):
    group_name = models.CharField(max_length=200)
    group_description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')  # Change 'todo_groups' to your preferred name

    class Meta:
        verbose_name='TodoGroup'
        
    def __str__(self):
        return self.group_name
    

    
class Tasks(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(null=True)
    assignee = models.ManyToManyField(User)
    files = models.FileField(upload_to='taskfiles/', blank=True, null=True)
    status_choices = (
        ('Incomplete', 'Incomplete'),
        ('Completed', 'Completed')
    )
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,related_name='created_by',null=True)
    completion_status = models.CharField(max_length=20, choices=status_choices, default='Incomplete')
    todo_group = models.ForeignKey(TodoGroups, on_delete=models.CASCADE, related_name='tasks',null=True)
    
    class Meta:
        verbose_name='Task'
        
    def __str__(self):
        return self.title


class Comments(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    task=models.ForeignKey(Tasks,on_delete=models.CASCADE,null=True)
    comment=models.TextField()
    class Meta:
        verbose_name='Comment'