
from multiprocessing.dummy import Process
from urllib.request import Request
from attr import field
from numpy import source
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from django.contrib.auth import get_user_model, password_validation
from django.db import models
from portfolio.models import Projects
from portfolio.models import DesignerPopol
from userReview.models import customerReview
from users.models import Client, Designer, User,Message
from client_commission.models import *
import datetime

class ClientUserSerializer(serializers.ModelSerializer):
    class Meta :
        model = Client
        fields = ('username','email','phone','company_name','description','profile_image')

class MyReviewBriefSerialzier(serializers.ModelSerializer):
    designer_username = serializers.CharField(source='designer.username')
    designer_profile_image = serializers.ImageField(source='designer.profile_image')

    brief_description = serializers.SerializerMethodField()
    brief_title = serializers.SerializerMethodField()
    class Meta :
        model = customerReview
        fields = (
            'id',
            'designer_username','designer_profile_image',
            'small_image',
            'brief_title','score','brief_description'
        )

    def get_brief_description(self, obj) :
        return obj.description[:100] + '...'
    
    def get_brief_title(self,obj) :
        return obj.title[:50] + '...'


class RequestedDesignerSerializer(serializers.ModelSerializer) :
    designer_username = serializers.CharField(source='designer.username')
    designer_average_stars = serializers.FloatField(source='designer.average_stars')
    designer_id = serializers.IntegerField(source = 'designer.id')
    designer_profile_image = serializers.ImageField(source= 'designer.profile_image')
    designer_portfolio_id =serializers.IntegerField(source='portfolio.id')
    class Meta  :
        model = RequestedDesigner
        fields = ('designer_portfolio_id','designer_username','designer_average_stars','designer_id','designer_profile_image','message')

class MyCommissionBriefSerializer(serializers.ModelSerializer) :
    brief_description = serializers.SerializerMethodField()
    request_designer = RequestedDesignerSerializer(many=True, read_only=True)
    designer_username = serializers.SerializerMethodField()
    # serializers.CharField(source='designer.username')
    class Meta :
        model = Commission
        fields = ('id','title', 'created','brief_description','budget','finish_date','small_image','request_designer','deadline','current_status','designer_username')
    def get_brief_description(self, obj) :
        return obj.description[:200] +'...'
        # description 을 200 글자만 표시할 수 있도록 바꾼다.
    def get_designer_username(self, obj) :
        if not obj.designer :
            return '디자이너가 아직 배정되지 않았습니다.'
        else :
            return obj.designer.username



class MyCommissionAlreadyStartedBriefSerializer(serializers.ModelSerializer) :
    brief_description = serializers.SerializerMethodField()
    designer_id = serializers.IntegerField(source = 'designer.id')
    designer_username = serializers.CharField(source='designer.username')
    designer_profile_image = serializers.ImageField(source= 'designer.profile_image')
    designer_average_stars = serializers.FloatField(source='designer.average_stars')

    class Meta :
        model = Commission
        fields = ('id','title', 'created','brief_description','budget','finish_date','small_image','designer_username','designer_id','designer_profile_image','designer_average_stars','deadline','current_status')
    def get_brief_description(self, obj) :
        return obj.description[:200] 
        # description 을 200 글자만 표시할 수 있도록 바꾼다.





class MyCommissionSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Commission
        fields = ('__all__')


class CommissionSerializer(serializers.ModelSerializer):
    auth_token = serializers.SerializerMethodField()

    class Meta:
         model = User
         fields = ('id', 'username','is_client','auth_token')
         read_only_fields = ('id', 'is_client')
    
    def get_auth_token(self, obj):
        try:
            token = Token.objects.get(user=obj)

        except Token.DoesNotExist:
            token = Token.objects.create(user=obj)

        return token.key
#---------------------------------------------------------------------

class DesignerUserSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Designer
        fields = ['username','email','phone','skills','description','profile_image','average_stars']

class PortfolioSerializer(serializers.ModelSerializer) :
    class Meta :
        model = DesignerPopol
        fields = ['description']

class PartInCommissionSerializer(serializers.ModelSerializer) :
    client_phone = serializers.CharField(source='client.phone')
    client_username = serializers.CharField(source='client.username')
    client_company_name = serializers.CharField(source='client.company_name')
    update_time = serializers.DateTimeField(source='updated',format="%Y-%m-%d %H:%M")
    class Meta :
        model = Commission
        fields = ['client_username','client_company_name','client_phone','title','budget','small_image','update_time']

class EndCommissionSerializer(serializers.ModelSerializer) :
    client_username = serializers.CharField(source='client.username')
    client_company_name = serializers.CharField(source='client.company_name')
    class Meta :
        model = Commission
        fields = ['client_username','client_company_name','title','budget','small_image','updated'] # 여기서 updated 는 마지막으로 수정 날짜 즉, 이 커미션이 종료된 날짜이다



class  ProjectSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Projects 
        fields = ('title','score','participation_date','client','id','small_image')

#--------------------------------------------------------------------


class MessageSerializer(serializers.ModelSerializer) :
    time = serializers.DateTimeField(source='created',format="%Y/%m/%d %H:%M")
    class Meta :
        model = Message
        fields = ('message', 'time','id')

class EmptySerializer(serializers.Serializer):
    pass