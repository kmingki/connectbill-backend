import os
from django.db import models
from users.models import Client,Designer
from portfolio.models import DesignerPopol
from uuid import uuid4

datetime_format = ["%Y-%m-%d"]


def path_and_rename_sumnail(instance, filename):
    upload_to = 'client_committion/committion_image/sumnail/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)

def path_and_rename_sumnail_panorama_image(instance, filename):
    upload_to = 'client_commission/commission_image/panorama_image'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)

class CommissionStatus(models.IntegerChoices):
    not_started  = 0
    not_started_not_selected = 1 # 마감기한 종료 후 디자이너 셀렉트 단계
    proceeding = 2 # 진행중
    finished = 3 # 끝
    finished_review = 4 # 리뷰까지 작성 완료

class Commission(models.Model) :
    client = models.ForeignKey(Client,on_delete=models.CASCADE)
    designer = models.ForeignKey(Designer, on_delete=models.CASCADE ,null = True, blank = True)

    small_image = models.ImageField(upload_to = path_and_rename_sumnail ,null = True ) # 썸네일용 이미지
    commission_image = models.FileField(upload_to=path_and_rename_sumnail_panorama_image, null = True) # 파노라마 이미지\

    title = models.CharField(max_length=300)    #의뢰서 제목
    description = models.TextField(null=True)   #의뢰서 상세 내용

    budget = models.IntegerField(null=False,blank=False) # 예산
    finish_date = models.IntegerField(null=False, blank=False) # 작업 기한 ( 기준 : 개월)
    deadline = models.CharField(max_length=50) #모집 마감 기한
    
    current_status = models.IntegerField(choices=CommissionStatus.choices, default = 0,blank=True) # 현재 상태 

    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)

    def __str__(self) :
        return self.title

    class Meta :
         verbose_name = 'Commission'


class RequestedDesigner(models.Model):
    commission = models.ForeignKey(Commission,on_delete=models.CASCADE,related_name='request_designer')
    designer = models.ForeignKey(Designer, on_delete=models.SET_NULL, null=True)
    message = models.TextField(max_length=300, blank= True)
    portfolio = models.ForeignKey(DesignerPopol,on_delete=models.SET_NULL,null=True)
