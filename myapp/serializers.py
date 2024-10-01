from rest_framework import serializers
from myapp.models import Todo, CustomUser
from rest_framework.validators import UniqueValidator 
from django.contrib.auth.password_validation import validate_password
from datetime import date  
from datetime import timedelta
from .serializers import *

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['id', 'task', 'detail', 'status', 'date_created', "due_date", "complete_date"]
        
    def create(self, validated_data):
        todays_date = date.today()
        validated_data['due_date'] = todays_date + timedelta(days=4)
        data = Todo.objects.create(**validated_data)
        return data

class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['id','task', 'detail', 'status']
        
class RegisterUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=CustomUser.objects.all())])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    def create(self, validated_data):
        user = CustomUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            full_name=validated_data['full_name']
        )
        user.set_password(validated_data['password'])
        user.save()    
        return user 
    
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'email', 'full_name']
      
    
class LoginUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'password']