from email.policy import default
from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import Designer,Client
from reborn.settings import MEDIA_URL

import os
default_profile_image =  os.path.join('/profile_image/user_default_image.png')

def get_and_authenticate_user(username, password):
    user = authenticate(username=username, password=password)
    if user is None:
        raise serializers.ValidationError("Invalid username/password. Please try again!")
    return user


def create_designer_account(username , email, password,password2 ,skills , phone,description):
    if password != password2 :
        raise serializers.ValidationError("password does not match")
    user = Designer.objects.create_user(
        username = username ,email=email,profile_image= default_profile_image, password=password,  skills = skills, phone = phone, description=description,is_client=False, average_stars = None)
    return user

def create_client_account(username , email, password,password2, company_name , phone,description):
    if password != password2 :
        raise serializers.ValidationError("password does not match")
    print('hello to check')
    user = Client.objects.create_user(
        username = username ,email=email, profile_image= default_profile_image,password=password, phone = phone , company_name = company_name, description=description,is_client=True)
    return user