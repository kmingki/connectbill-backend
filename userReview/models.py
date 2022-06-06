import os
from django.db import models
from uuid import uuid4
from django.core.validators import MinValueValidator, MaxValueValidator

from client_commission.models import Commission
from users.models import Designer, Client

def path_and_rename_sumnail(instance, filename):
    upload_to = 'userReview/customerReview_Image/sumnail/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)

def path_and_rename_panorama_image(instance, filename):
    upload_to = 'userReview/customerReview_Image/panorama_image/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)


class customerReview(models.Model) :
    score = models.IntegerField(default = 0,validators=[MinValueValidator(0), MaxValueValidator(5)])
    small_image = models.ImageField(upload_to=path_and_rename_sumnail)
    panorama_image = models.ImageField( height_field=None, width_field=None, max_length=100, upload_to=path_and_rename_panorama_image)
    client = models.ForeignKey(Client,on_delete=models.CASCADE)
    designer = models.ForeignKey(Designer, on_delete= models.SET_NULL, null=True)
    description = models.TextField(null =True)
    commission = models.ForeignKey(Commission, null = True,on_delete= models.SET_NULL)
    title = models.CharField(max_length = 50 , default=None,blank=True)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)


    def __str__(self) :
        return self.description[:10]

    class Meta :
         verbose_name = 'customerReview'
