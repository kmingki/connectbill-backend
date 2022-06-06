from rest_framework.authtoken.models import Token

from rest_framework import viewsets,status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from rest_framework.decorators import api_view, permission_classes

from rest_framework import generics , status

from uuid import uuid4

from portfolio.models import DesignerPopol,Projects,Certificate, EducationAndCareer
from Mypage import serializers
from .serializers import ProjectSerializer, PopolSerializer,BriefPopolSerializer,CertificateSerializer, EduAndCareerSerializer, ProjectSerializer
from rest_framework import status

from users.models import *
import cv2
import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import numpy as np
from reborn import settings

MEDIA_ROOT = settings.STATIC_URL


@api_view(['GET'])
@permission_classes([AllowAny])
def portfolio_view(request):
    ListPopol = DesignerPopol.objects.all()
        
    briefportfolio = BriefPopolSerializer(ListPopol, many = True)

    for i in range(0,len(briefportfolio.data)) :
        if len(briefportfolio.data[i]['projects']) > 3 :
            briefportfolio.data[i]['projects'] = briefportfolio.data[i]['projects'][:3]
    
    return Response(briefportfolio.data, status = status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def portfolio_view_detail(request, pk):
    Popol = DesignerPopol.objects.get(id = pk)
    serializer_popol = PopolSerializer(Popol, many = False)

    certifits = Certificate.objects.filter(portfolio= Popol)
    serializer_certificate = CertificateSerializer(certifits, many= True)

    eduandcareers = EducationAndCareer.objects.filter(portfolio= Popol)
    serializer_educareer = EduAndCareerSerializer(eduandcareers, many=True)

    projects = Projects.objects.filter(portfolio= Popol)
    serializer_projects = ProjectSerializer(projects, many=True)

    
    return Response(
        {
            'portfolio' : serializer_popol.data , 
            'certificates' : serializer_certificate.data,
            'educationandcareer' : serializer_educareer.data ,
            'projects' : serializer_projects.data ,
        }
        , status = status.HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated, ])
def create_portfolio(request):
    designer = Designer.objects.get(id = request.user.id)

    if request.user.is_client == False :

            newPortfolio = DesignerPopol(
                designer = designer,
                description = request.data['content']
            )
            newPortfolio.save()

            for i in request.data['certificates'] :
                newCertificate = Certificate(
                    portfolio = newPortfolio,
                    acquired_date = i['acquired_period'],
                    certificate_name = i['certificate_name'],
                    time = i['time']
                )
                newCertificate.save()

            for j in request.data['educationcareers'] :
                newEducationAndCareer = EducationAndCareer(
                    portfolio = newPortfolio,
                    working_period = j['working_period'],
                    company_name = j['company_name'],
                    description = j['job_position']
                )
                newEducationAndCareer.save()
        
            return Response({'result':'success', 'message': '성공적으로 등록되었습니다.'}, status=status.HTTP_201_CREATED) #json?

    else :
        return Response({'result':'fail', 'message': '디자이너가 아니십니다'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated, ])
def create_project(request):
    tmpdesigner= Designer.objects.get(id = request.user.id)
    tmpportfolio = DesignerPopol.objects.get(designer= tmpdesigner)

    if request.user.is_client == False :
        newProject = Projects(
            title = request.data['title'],
            small_image = request.data['title_image'],
            description = request.data['description'],
            participation_date = request.data['start_date'],
            portfolio = tmpportfolio,
        )
        newProject.save()
    else :
        return Response({"message" : 'failed to make projects'},status= status.HTTP_204_NO_CONTENT)
    return Response({'message': 'success'}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny, ])
def project_view_detail(request,pk):
    project= Projects.objects.get(id = pk)
    projectSerializer = ProjectSerializer(project, many=False)
   
    return Response({'project': projectSerializer.data}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated, ])
def image_handler(request):
    #print(request.data['files'])
    image = request.FILES['files'] # or self.files['image'] in your form
    filename = request.FILES['files']
    user = User.objects.get(id = request.user.id)  
    img = (ContentFile(image.read()))
    path = default_storage.save('project_image/'+str(user.username)+'/'+ str(uuid4().hex)+'.jpg', img)
    path1 = os.path.join(MEDIA_ROOT,path)
    
    # img_array = np.fromfile(path1, np.uint8)
    # img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    img = cv2.imread(path1)
    img = cv2.resize(img, dsize=(500, 500), fx=0.3, fy=0.7, interpolation=cv2.INTER_AREA)# 
    
    cv2.imwrite(path1,img)

    print (path)
    return Response({'file_path' :'media/'+path})



        




# @api_view(['POST'])
# def updatePortfolio(request): 
#     try:
#         user = User.objects.get(user_id=request.data['userid'])
#     except:
#         return Response({'result':'fail', 'message': '존재하지 않는 사용자입니다.'}, status=status.HTTP_404_NOT_FOUND)

#     try:
#         portfolio = DesignerPopol.objects.get(id=request.data['id'])
#     except:
#         return Response({'result':'fail', 'message': '존재하지 않는 게시글 입니다.'}, status=status.HTTP_404_NOT_FOUND)

#     portfolio.title = request.data['title']
#     portfolio.description = request.data['description']
#     portfolio.image = request.data['image']
#     serializer = PopolTestSerializer(data=request.data) #request.data = querydict
    
#     if serializer.is_valid():
#         portfolio.save()
#     else:
#         print(serializer.errors)
#         return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

#     return Response({'result':'success', 'message': '성공적으로 수정되었습니다.'}, status=status.HTTP_201_CREATED) 

# #parameter로 
# @api_view(['DELETE'])
# def deletePortfolio(request, id): 

#     try:
#         portfolio = DesignerPopol.objects.get(id=id)
#     except:
#         return Response({'result':'fail', 'message': '존재하지 않는 게시글입니다.'}, status=status.HTTP_404_NOT_FOUND)

#     print(portfolio.delete())

#     return Response({'result':'success', 'message': '성공적으로 등록되었습니다.'}, status=status.HTTP_200_OK) 
