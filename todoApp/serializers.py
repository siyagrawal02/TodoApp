from todoApp.models import User,Tasks,TodoGroups,Comments
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
import secrets

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields="__all__"
    
    def validate_email(self, value):
        """
        Validate that the email is unique.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def validate_password(self, value):
        """
        Validate the strength of the password.
        """
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(str(e))
        return value

    def validate(self, data):
        """
        Validate the entire serializer data, e.g., check for unique combinations.
        """
        # You can add additional validation logic here if needed.
        return data
    

class TodoGroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model=TodoGroups
        fields="__all__"
        
        
class TasksSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Tasks
        fields="__all__"
        
    def validate(self, data):
        # Perform additional validation here
        required_fields = ['title', 'description','due_date','assignee','files','created_by','completion_status','todo_group']  # Add all your required field names here

        for field_name in required_fields:
            if field_name not in data or data[field_name] is None:
                raise serializers.ValidationError({field_name: 'This field is required.'})

        return data
  
    
class OverdueTasksSerializer(serializers.ModelSerializer):
    class Meta:
        model=Tasks
        fields="__all__"
        
class UpdateTaskStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model=Tasks
        fields=['id','completion_status']
        
    def validate(self, data):
        # Perform additional validation here
        required_fields = ['completion_status']  # Add all your required field names here

        for field_name in required_fields:
            if field_name not in data or data[field_name] is None:
                raise serializers.ValidationError({field_name: 'This field is required.'})

        return data
    def update(self, instance, validated_data):
        instance.completion_status = validated_data.get('completion_status', instance.completion_status)
        instance.save()
        return instance
    
class AddCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comments
        fields="__all__"
    
    def validate(self, data):
        # Perform additional validation here
        required_fields = ['user','task','comment']  # Add all your required field names here

        for field_name in required_fields:
            if field_name not in data or data[field_name] is None:
                raise serializers.ValidationError({field_name: 'This field is required.'})

        return data


      
        
class AssigneeMgmtSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    username=serializers.CharField()
    task_id = serializers.IntegerField()
 
class UserRegisterDocSerializer(serializers.Serializer):
    username=serializers.CharField()
    email=serializers.EmailField()
    password=serializers.CharField()

class TodoGroupDocSerializer(serializers.Serializer):
    group_name=serializers.CharField()
    group_description=serializers.CharField()
    user=serializers.IntegerField()
    
class TasksDocSerializer(serializers.Serializer):
    title=serializers.CharField()
    description=serializers.CharField()
    due_date=serializers.DateField()
    assignee=serializers.IntegerField()
    files=serializers.FileField()
    created_by=serializers.IntegerField()
    completion_status=serializers.CharField()
    todo_group=serializers.IntegerField()
        