
from django.core.exceptions import ImproperlyConfigured
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .utils import get_and_authenticate_user, create_designer_account,  create_client_account
from django.contrib.auth import get_user_model, logout, login

from . import serializers
from .utils import get_and_authenticate_user

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import cv2,os
import numpy as np
from reborn import settings

MEDIA_ROOT = settings.STATIC_URL


User = get_user_model()

class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny, ]
    serializer_class = serializers.EmptySerializer
    serializer_classes = {
        'login': serializers.UserLoginSerializer,
        'register_designer': serializers.DesignerRegisterSerializer,
        'register_client' : serializers.ClientRegisterSerializer,
        'password_change': serializers.PasswordChangeSerializer,
    }

    @action(methods=['POST', ], detail=False)
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_and_authenticate_user(**serializer.validated_data)
        data = serializers.AuthUserSerializer(user).data
        return Response(data=data, status=status.HTTP_200_OK)

    @action(methods=['POST', ], detail=False)
    def register_designer(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print('check')
        print(serializer.validated_data)
        user = create_designer_account(**serializer.validated_data)

        data = serializers.DesignerRegisterSerializer(user).data
        return Response(data=data, status=status.HTTP_201_CREATED)
    
    @action(methods=['POST', ], detail=False)
    def register_client(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = create_client_account(**serializer.validated_data)
        data = serializers.ClientRegisterSerializer(user).data
        return Response(data=data, status=status.HTTP_201_CREATED)

    @action(methods=['POST', ], detail=False)
    def logout(self, request):
        logout(request)
        data = {'success': 'Sucessfully logged out'}
        return Response(data=data, status=status.HTTP_200_OK)
    
    @action(methods=['POST'], detail=False, permission_classes=[IsAuthenticated, ])
    def password_change(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['POST'], detail=False, permission_classes=[IsAuthenticated,])
    def profile_image_change(self,request) :
        
        image= request.data['new_profile_image']
        img = (ContentFile(image.read()))
        path = default_storage.save('profile_image/'+str(request.user.username)+'/'+ str(image), img)
        path1 = os.path.join(MEDIA_ROOT,path)
        
        img_array = np.fromfile(path1, np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        # img = cv2.imread(path1)
        img = cv2.resize(img, dsize=(256, 256), fx=0.3, fy=0.7, interpolation=cv2.INTER_AREA)# 

        request.user.profile_image = img 
        request.user.save()
        return Response(status=status.HTTP_200_OK)
        


    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured("serializer_classes should be a dict mapping.")

        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()

    