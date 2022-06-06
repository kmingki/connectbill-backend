from rest_framework.authtoken.models import Token
from rest_framework import serializers
from django.db import models
from users.models import *
from .models import *
from django.forms import ValidationError

class EmptySerializer(serializers.Serializer):
    pass

class CommissionSerializer(serializers.ModelSerializer):

    class Meta:
         model = Commission
         fields = ('id','title','finish_date','budget','description','small_image','commission_image')
        #  read_only_fields = ('id', 'is_client')
    
    # def get_panorama_image(self,obj):
    def validate_title(self, value):
        if value=='' or len(value)> 100 :
            raise ValidationError('Not Validate title')
        return value        


class CommissionViewDetailSerializer(serializers.ModelSerializer):
    client_username = serializers.CharField(source='client.username')
    client_company_name = serializers.CharField(source='client.company_name')
    client_profile_image = serializers.ImageField(source='client.profile_image')
    class Meta:
         model = Commission
         fields = ('id','title','finish_date','budget','description','current_status','deadline','commission_image','client_username','client_company_name','client_profile_image')
        #  read_only_fields = ('id', 'is_client')
    

class CommissionViewSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.username')
    client_company_name = serializers.CharField(source='client.company_name')
    client_profile_image = serializers.ImageField(source = 'client.profile_image')
    class Meta :
        model = Commission
        fields = ('id','title', 'client_profile_image','deadline','budget','finish_date','small_image','client_company_name','client_name')

    




    # def get_brief_description(self, obj) :
    #     return obj.description[:50] 
        # description 을 50 글자만 표시할 수 있도록 바꾼다.
