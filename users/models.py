from django.db import models

from django.db.models.signals import post_save
from django.core.validators import MinValueValidator, MaxValueValidator


from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token




class User(AbstractUser) :
    is_Designer = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)
    profile_image = models.ImageField(null=True)


class Client(User,models.Model) :
    company_name=models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    description =models.TextField(null= True)
    USERNAME_FIELD: User.username

    def __str__(self):
        return self.username 
        
    class Meta :
            verbose_name = 'Client'

class Designer(User,models.Model) :
    phone = models.CharField(max_length=100, blank=True)
    average_stars = models.FloatField(null=True,default=None, blank=True)
    skills = models.CharField(max_length=100,blank=True)
    description = models.TextField(null=True, blank=True)

    USERNAME_FIELD: User.username

    def __str__(self) :
        return self.username
    
    class Meta :
        verbose_name = 'Designer'
    # def __unicode__(self):

# class ProcessingCommission(models.Model) :
#     designer = models.ForeignKey(Designer, on_delete=models.CASCADE)
#     commission = models.ForeignKey('client_commission.Commission', on_delete=models.CASCADE)

class Message(models.Model) :
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add = True)
    count = models.IntegerField(default = 0, blank =True, null=True)


class DesignerReview(models.Model) :
    review_text = models.TextField(max_length=200)
    designer = models.ForeignKey(Designer,on_delete=models.CASCADE)
    score = models.IntegerField(default = 0,validators=[MinValueValidator(0), MaxValueValidator(5)],blank=True)
    commission = models.ForeignKey('client_commission.Commission', on_delete=models.SET_NULL, null =True)


    # def __unicode__(self):
    #     return self.user.username+"Client"   

# Create your models here.
