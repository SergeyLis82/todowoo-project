from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class tasktodo(models.Model):
    title = models.CharField(max_length=150)
    memo = models.TextField(blank=True)
    important = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    completed = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title