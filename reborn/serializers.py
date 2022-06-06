from rest_framework import serializers
from users.models import User,Designer,Client
from userReview.models import customerReview
from portfolio.models import DesignerPopol

class designerSerializer(serializers.ModelSerializer):
    profile_image = serializers.ImageField(source='designer.profile_image')
    username = serializers.CharField(source='designer.username')
    average_stars = serializers.IntegerField(source='designer.average_stars')
    
    class Meta : 
        model = DesignerPopol
        fields = ['id','profile_image','designer','username', 'average_stars']



class reviewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='client.username')
    userProfileImage = serializers.ImageField(source = 'client.profile_image')
    companyName = serializers.CharField(source= 'client.company_name')
    brief_description = serializers.SerializerMethodField()
    class Meta :
        model = customerReview
        fields = ['brief_description','small_image','client','username','userProfileImage','companyName','score']

    def get_brief_description(self, obj) :
        return obj.description[:50] + '...'    
