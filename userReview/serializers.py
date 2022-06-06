from jsonschema import ValidationError
from numpy import source
from rest_framework import serializers

from users.models import DesignerReview
from .models import customerReview

class EmptySerializer(serializers.Serializer):
    pass

class ReviewSerializer(serializers.ModelSerializer):
    class Meta :
        model = customerReview
        fields = ['title','score','panorama_image','small_image','description']
    
    def validated_title(self, value):
        if value == '' or len(value) > 50 :
            raise ValidationError("invalid title")
        return value 

class BriefReviewSerializer(serializers.ModelSerializer):
    client_username = serializers.CharField(source='client.username')
    client_profile_image = serializers.ImageField(source = 'client.profile_image')
    client_company_name = serializers.CharField(source= 'client.company_name')

    designer_username = serializers.CharField(source='designer.username')
    designer_profile_image = serializers.ImageField(source='designer.profile_image')

    brief_description = serializers.SerializerMethodField()
    brief_title = serializers.SerializerMethodField()
    class Meta :
        model = customerReview
        fields = (
            'id',
            'designer_username','designer_profile_image',
            'small_image','client_username','client_profile_image','client_company_name',
            'brief_title','score','brief_description'
        )

    def get_brief_description(self, obj) :
        return obj.description[:100] + '...'
    
    def get_brief_title(self,obj) :
        return obj.title[:50] + '...'
        
    

class ReviewDetailSerializer(serializers.ModelSerializer):
    client_profile_image = serializers.ImageField(source='client.profile_image')
    client_username = serializers.CharField(source='client.username')
    client_company_name = serializers.CharField(source='client.company_name')
    client_email = serializers.EmailField(source='client.email')

    commission_image = serializers.FileField(source='commission.commission_image')
    commission_budget = serializers.IntegerField(source='commission.budget')
    commission_description = serializers.CharField(max_length=500)

    class Meta :
        model = customerReview
        fields = (
            'client_profile_image','client_username',
            'client_company_name','client_email',
            'panorama_image','score',
            'description', 'title',
            'created',
            'commission_image','commission_budget' ,'commission_description'
        )

class DesignerReviewSerializer(serializers.ModelSerializer) :
    designer_username = serializers.CharField(source= 'designer.username')
    designer_id = serializers.IntegerField(source='designer.id')
    designer_email =serializers.EmailField(source='designer.email')
    designer_profile_image = serializers.ImageField(source='designer.profile_image')
    class Meta :
        model = DesignerReview
        fields = ('designer_username','designer_id','designer_emai','designer_profile_image','score','review_text')
    