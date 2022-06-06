from email.policy import HTTP
import imp
from this import d
import certifi
from django.http import QueryDict
from django.shortcuts import render
from pyrsistent import v
from portfolio.models import DesignerPopol, Projects
from portfolio.serializers import BriefPopolSerializer,ClientProfileSerializer
from rest_framework.response import Response
from rest_framework import  status
from client_commission.models import RequestedDesigner
from portfolio.models import Certificate, EducationAndCareer
from portfolio.serializers import CertificateSerializer, EduAndCareerSerializer
from users.models import *
from userReview.models import customerReview
from client_commission.models import Commission
from client_commission.serializers import CommissionSerializer

from portfolio.serializers import PopolSerializer, DesignerProfileSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from .serializers import MyCommissionAlreadyStartedBriefSerializer, MessageSerializer,PortfolioSerializer,ProjectSerializer,MyCommissionBriefSerializer,MyCommissionSerializer,MyReviewBriefSerialzier, ClientUserSerializer,DesignerUserSerializer,PartInCommissionSerializer,EndCommissionSerializer
from django.db.models import Q

#from users.serializers import ClientProfileImageUpdateSerializer

from datetime import datetime

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request, format=None):
    messages = Message.objects.filter(user = request.user)
    if not messages :
        pass
    else :
        for message in messages :
            message.count = message.count + 1
            print('check')
            if message.count >5 :
                message.delete()
                continue
            message.save()
    
    messageSerializer = MessageSerializer(messages, many=True)
   
    if request.user.is_client == True :
        clientUser = Client.objects.get(id = request.user.id)
        userSerializer = ClientUserSerializer(clientUser, many=False)

        my_commission_not_started  = Commission.objects.filter(Q(client = clientUser) & (Q(current_status= 0)|Q(current_status=1)))
        my_commission_not_startedSerializer =  MyCommissionBriefSerializer(my_commission_not_started, many= True)
        
        my_review = customerReview.objects.filter(client= clientUser)
        my_reviewSerializer = MyReviewBriefSerialzier(my_review, many = True)

        my_commission_started = Commission.objects.filter(Q(client = clientUser) & (Q(current_status= 2)|Q(current_status=3)))
        if my_commission_started.count()== 0 :
            return Response({
            'user' : userSerializer.data,
            'commissions_not_started' : my_commission_not_startedSerializer.data,
            'commissions_started' : None ,
            'reviews' :  my_reviewSerializer.data,
            'messages' : messageSerializer.data,
        })

        my_commission_startedSerializer = MyCommissionAlreadyStartedBriefSerializer(my_commission_started, many= True)
                
        return Response({
            'user' : userSerializer.data,
            'commissions_not_started' : my_commission_not_startedSerializer.data,
            'commissions_started' :  my_commission_startedSerializer.data,
            'reviews' :  my_reviewSerializer.data,
            'messages' : messageSerializer.data,
        })

    else :
        designerUser = Designer.objects.get(id = request.user.id)
        userserializer = DesignerUserSerializer(designerUser,many= False)

        try:      
            portfolio = DesignerPopol.objects.get(designer = designerUser )
        except :
            return Response(
                {'user' : userserializer.data}
            )

        else :
            portfolioSerializer = PortfolioSerializer(portfolio, many= False)


            certificates = Certificate.objects.filter(portfolio = portfolio)
            certificateSerializer = CertificateSerializer(certificates, many= True)

            eduandcareers = EducationAndCareer.objects.filter(portfolio= portfolio)
            eduAndCareerSerializer = EduAndCareerSerializer(eduandcareers,many= True)

            partincommission = Commission.objects.filter(designer_id = request.user.id , current_status=2)
            partincommissionSerializer = PartInCommissionSerializer(partincommission, many=True)
            
            for i in partincommissionSerializer.data :
                obj=datetime.strptime(i['update_time'],'%Y-%m-%d %H:%M')
                print(datetime.now())
                print(obj)
               
                tmp = datetime.now() - obj
                # print(tmp)
                i['update_time'] = str(tmp)

            endcommission = Commission.objects.filter(Q(designer_id = request.user.id) & (Q(current_status = 3) | Q(current_status=4) ))
            endcommissionSerializer = EndCommissionSerializer(endcommission, many=True)

            projects = Projects.objects.filter(portfolio = portfolio)
            projectSerializer = ProjectSerializer(projects, many=True)
            print( {
                    'user' : userserializer.data,
                    'portfolio' :portfolioSerializer.data,
                    'certificates' : certificateSerializer.data,
                    'educationandcareers' : eduAndCareerSerializer.data,
                    'part_in_commission':partincommissionSerializer.data,
                    'projects' :projectSerializer.data,
                    'end_commission' : endcommissionSerializer.data,
                    'messages' : messageSerializer.data,
                })
            return Response(
            
                {
                    'user' : userserializer.data,
                    'portfolio' :portfolioSerializer.data,
                    'certificates' : certificateSerializer.data,
                    'educationandcareers' : eduAndCareerSerializer.data,
                    'part_in_commission':partincommissionSerializer.data,
                    'projects' :projectSerializer.data,
                    'end_commission' : endcommissionSerializer.data,
                    'messages' : messageSerializer.data,
                }
            )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMyInfo(request, format=None):
    if request.user.is_client == True :
        tmpuserProfile = Client.objects.get(id = request.user.id)
        userserializer = ClientProfileSerializer(tmpuserProfile,many= False)

        my_commission  = Commission.objects.filter(client = tmpuserProfile)
        my_commissionSerializer =  MyCommissionBriefSerializer(my_commission, many= True)
        return Response(
            userserializer.data,
            my_commissionSerializer.data
        )

    else :
        tmpuserProfile = Designer.objects.get(auth_token = request.auth)
        userserializer = DesignerProfileSerializer(tmpuserProfile,many= False)
        return Response(
           userserializer.data,
        )

'''
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def profile_update(request, pk) :
    if request.user.is_client == True :

        modelObject = Client.objects.get(pk= pk)
        serializer = ClientProfileImageUpdateSerializer( modelObject, data=request.data, partial=True) # set partial=True to update a data partially
    if serializer.is_valid():
        serializer.save()
        return Response(status =201, data=serializer.data)
    return Response(status=400, data="wrong parameters")
'''

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def designer_selected_for_commission(request) :
    if request.user.is_client == True :
        commission = Commission.objects.get(id = request.data['commission_id'])
        designer =Designer.objects.get(id= request.data['designer_id'])
        commission.designer = designer
        commission.current_status = 2
        commission.save(update_fields=['designer','current_status'])

        selectedUser = User.objects.get(id = request.data['designer_id'])
        # newProcessingCommission = ProcessingCommission(
        #     designer = designer,
        #     commission = commission
        # )
        # newProcessingCommission.save()


        newMessage = Message(
            user = selectedUser,
            message = str(selectedUser.username) + "님이 '" + str(commission.title)  +"' 의뢰에 선택되셨습니다."
        )
        
        newMessage.save()

        RequestedDesigner.objects.filter(commission= commission).delete()

        return Response(status=status.HTTP_200_OK)
    else :
        return Response({'message':'Designer can not select'},status=status.HTTP_403_FORBIDDEN)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_message(request) :
    message = Message.objects.get(id = request.data['msg_id'])
    message.delete()
    return Response(status=status.HTTP_200_OK)



# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def delete_my_commission(request,pk) :
#     if request.user.is_client == True :
#         commission = Commission.objects.get(id = pk)
#         commission.delete()
#         return Response(status=status.HTTP_200_OK)
    

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def detail_my_portfolio(request,pk) :
#     Popol = DesignerPopol.objects.get(id = pk)
#     serializer = PopolSerializer(Popol, many = False)
#     return Response(serializer.data)

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def detail_my_commission(request,pk) :
#     commission = Commission.objects.get(id = pk)
#     serializer = MyCommissionSerializer(commission, many = False)

#     selected_designer={}
#     for i in commission.request_designer_id :
#         tmp = Designer.objects.get(id = i)
#         selected_designer.append({'username':tmp.username,'id' :tmp.id})

#     return Response(
#         serializer.data,
#         {
#             'selected_designer':selected_designer
#         }
#     )


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def delete_portfolio(request,pk) :
#     portforlio = DesignerPopol.objects.get(pk=pk)
#     portforlio.delete()
#     return Response(status=status.HTTP_200_OK)





