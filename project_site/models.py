from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Database_user(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False, null=True)
    gender = models.CharField(max_length=50,default="Gender")
    highest_qualification=models.CharField(max_length=50)
    contact=models.CharField(max_length=20)
    bio = models.TextField(max_length=1000)
    image_dp=models.TextField(null=True,blank=True)
    

    


