from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta, date

class Packages(models.Model):
    Package_name=models.CharField(max_length=255)
    Package_fee=models.IntegerField()
   
    Package_description=models.TextField()

class Maritalstatus(models.Model):
    Status = models.CharField(max_length=255)

    def __str__(self):
        return self.Status

class Religion(models.Model):
    Religion_name=models.CharField(max_length=255)
    def __str__(self):
        return self.Religion_name

class Cast(models.Model):
    Religion = models.ForeignKey(Religion,on_delete=models.CASCADE,null=True)
    Cast = models.CharField(max_length=255)
    def __str__(self):
        return self.Cast
    
class Usermember(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    Member_id = models.IntegerField(null=True)
    Status = models.CharField(max_length=255)
    Age = models.IntegerField()
    Height = models.IntegerField()
    Gender = models.CharField(max_length=30)
    Place = models.CharField(max_length=255)
    District = models.CharField(max_length=255)
    Designation = models.CharField(max_length=255)
    Contact = models.CharField(max_length=255)
    religion = models.ForeignKey(Religion,on_delete=models.CASCADE,null=True)
    cast = models.ForeignKey(Cast,on_delete=models.CASCADE,null=True)
    Father_name=models.CharField(max_length=255)
    Father_occupation = models.CharField(max_length=255)
    Mother_name= models.CharField(max_length=255)
    Mother_occupation = models.CharField(max_length=255)
    Sibling_name = models.CharField(max_length=255)
    Sibling_status = models.CharField(max_length=30)
    Joining_date = models.DateField()
    images = models.ManyToManyField('Image', blank=True)
    is_approved = models.BooleanField(default=False)
    package_expired = models.BooleanField(default=False)
    

class Image(models.Model):
    image = models.ImageField(upload_to='images/')
class Payment(models.Model):
    package = models.ForeignKey(Packages,on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(Usermember,on_delete=models.CASCADE,null=True)
    Payment_method = models.CharField(max_length=50)
    


