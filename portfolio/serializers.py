from django.forms import ValidationError
from rest_framework import serializers
from . models import Certificate, DesignerPopol, EducationAndCareer,Projects
from users.models import User,Designer,Client

class PopolSerializer(serializers.ModelSerializer):
    designer_username = serializers.CharField(source= 'designer.username')
    designer_id = serializers.IntegerField(source='designer.id')
    designer_email =serializers.EmailField(source='designer.email')
    designer_phone = serializers.IntegerField(source='designer.phone')
    designer_profile_image = serializers.ImageField(source='designer.profile_image')
    designer_average_stars = serializers.IntegerField(source='designer.average_stars')
    desinger_skills = serializers.CharField(source='designer.skills')
    class Meta :
        model = DesignerPopol
        fields = ('designer_username','desinger_skills','designer_id','designer_email','description','designer_phone','designer_profile_image','designer_average_stars')

    def validate_title(self, value):
        if value=='':
            raise ValidationError('제목은 필수 항목입니다.')
        return value

class  CertificateSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Certificate
        fields= ('acquired_date','certificate_name','time')

class EduAndCareerSerializer(serializers.ModelSerializer) :
    class Meta :
        model = EducationAndCareer
        fields = ('working_period','company_name','description')


class ProjectSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Projects
        fields = ('id','title','description','participation_date', 'client', 'score','small_image')
    
    def validate_title(self, value):
        if value=='':
            raise ValidationError('제목은 필수 항목입니다.')
        return value

class BriefProjectSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Projects
        fields = ['title', 'score']



class BriefPopolSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='designer.username')
    profile_image = serializers.ImageField(source = 'designer.profile_image')
    skills = serializers.CharField(source='designer.skills')
    average_stars = serializers.IntegerField(source = 'designer.average_stars')
    projects = BriefProjectSerializer(many=True, read_only=True)
    class Meta : 
        model = DesignerPopol
        fields = ['id','username','profile_image','skills','average_stars','description','projects']





class DesignerProfileSerializer(serializers.ModelSerializer) :
    # employer  = ClientSerializer(many=False,read_only=True)

    class Meta:
        model = Designer
        fields = ['username','email','skills','phone','description','skills','average_stars']

class ClientProfileSerializer(serializers.ModelSerializer) :
    #popols = serializers.RelatedField(many=True,read_only=True)
    #designer = DesignerSerializer(read_only=True)
    # employer  = ClientSerializer(many=False,read_only=True)

    class Meta:
        model = User
        fields = ['username','email']



# class PopolTestSerializer(serializers.ModelSerializer):
#     class Meta :
#         model = DesignerPopol
#         # exclude = ('user', )
