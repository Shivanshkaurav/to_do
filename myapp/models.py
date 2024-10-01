from django.db import models
from django.contrib.auth.models import AbstractUser

STATUS = (("Pending", "Pending"), ("In Progress", "In Progress"), ("Completed", "Completed"))

class Todo(models.Model):
    user = models.ForeignKey("CustomUser", on_delete=models.CASCADE)
    task = models.CharField(max_length=1000)
    detail = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=100, choices=STATUS, default="Pending")
    date_created = models.DateTimeField(auto_now=True)
    due_date = models.DateField(null=True, blank=True)
    complete_date = models.DateField(null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Todo"
    def __str__(self):
        return self.task  

class CustomUser(AbstractUser):
    email = models.EmailField(max_length=254, unique=True,null=True,blank=True)
    full_name = models.CharField(max_length=100)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'full_name']

    def __str__(self):
        return self.username