

from django.core.exceptions import ImproperlyConfigured
from django.db.models import  Count
from rest_framework import viewsets, status

from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model, logout, login

from rest_framework.decorators import api_view
from portfolio.models import Projects

from users.models import Designer,Message,User
from portfolio.models import DesignerPopol
from userReview.models import customerReview

from .serializers import designerSerializer as dS, reviewSerializer as rS



@api_view(['GET'])
def index(request):
      tmpportfolio = DesignerPopol.objects.all()
      tmpportfolio = tmpportfolio.reverse()[:5]
      portfolio_list = dS(tmpportfolio , many= True)

      reviews = customerReview.objects.all().reverse()[:5]
      reviews_list = rS(reviews , many= True)

      return Response(
         {
         'designer' :portfolio_list.data,
         
         'reviews':reviews_list.data,
         
         }
      )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def menu(request):
            
      user = User.objects.get(id = request.user.id)
      messages = Message.objects.filter(user = user)
      flag =0
      if messages.count() == 0 :
             flag = 1

      Response({'flag': flag})
