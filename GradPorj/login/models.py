from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default= None)
    stdid= models.CharField(max_length=7, default= None)
    Name= models.CharField(max_length=100, default= None)

class Secretary(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default= None)
    secid= models.CharField(max_length=7, default= None)
    Name= models.CharField(max_length=100, default= None)

class staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default= None)
    secid= models.CharField(max_length=7, default= None)
    Name= models.CharField(max_length=100, default= None)

class Advisor(models.Model):
    Advise = models.OneToOneField(Student, on_delete=models.CASCADE, default= None)
    Advising = models.ManyToOneRel(staff, on_delete=models.CASCADE, to= Advise, field_name= Advise)
    Name = models.CharField(max_length = 100, default = None)
    stdid = models.CharField(max_length=7, default= None)
    secid= models.CharField(max_length=7, default= None)

class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    stdid= models.CharField(max_length=7, default= None)
    type= models.CharField(max_length=100, default= None)
    status = models.CharField(max_length=100, default="Pending")
    location = models.CharField(max_length=100, default= None)
    history = models.CharField(max_length=50000, default = None)
    Date = models.DateField(auto_now_add=True)
    barcode = models.CharField(max_length= 100, default=None)
    vicestatus = models.CharField(max_length=100, default="Not received")
    chairstatus = models.CharField(max_length=100, default="Not received")
    Advisorstatus = models.CharField(max_length=100, default="Not received")
    flag = models.CharField(max_length=100, default=None)


class Chairman(models.Model):
    staf = models.OneToOneField(staff, on_delete=models.CASCADE, default= None)

class Vicechairman(models.Model):
    staf = models.OneToOneField(staff, on_delete=models.CASCADE, default= None)

class secnotification(models.Model):
    text= models.CharField(max_length= 100, default=None)
    stdid = models.CharField(max_length=100, default=None)
    Date = models.DateField(auto_now_add=True)
    type = models.CharField(max_length=100, default=None)
class stdnotification(models.Model):
    text = models.CharField(max_length=100, default=None)
    Date = models.DateField(auto_now_add=True)
    stdid = models.CharField(max_length=100, default=None)

class staffnotification(models.Model):
    text = models.CharField(max_length=100, default=None)
    Date = models.DateField(auto_now_add=True)
    stdid = models.CharField(max_length=100, default=None)
    secid = models.CharField(max_length=100, default=None)
