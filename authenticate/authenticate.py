
from django.contrib.auth import backends
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.conf import settings
import datetime, jwt


from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, CSRFCheck


User = get_user_model()


def generate_access_token(user):
    access_token_payload = {
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(
            days=0, minutes=60
        ),
        'iat': datetime.datetime.utcnow(),
    }
    
    access_token = jwt.encode(
        access_token_payload,
        settings.SECRET_KEY, algorithm='HS256'
    ).decode('utf-8')
    
    return access_token
    
    
def generate_refresh_token(user):
    refresh_token_payload = {
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
        'iat': datetime.datetime.utcnow(),
    }
    
    refresh_token = jwt.encode(
        refresh_token_payload,
        settings.REFRESH_TOKEN_SECRET, algorithm='HS256'
    ).decode('utf-8')
    
    return refresh_token


def jwt_login(response, user):
    access_token = generate_access_token(user)
    refresh_token = generate_refresh_token(user)
    
    data = {
        'username' : user.username,
        'access_token': access_token,
        'refresh_token' : refresh_token
    }
    
    response.data = data
    response.set_cookie(key="refreshtoken", value=refresh_token, httponly=True)
    
    return response

# class EmailorUsernameAuthBackend(backends.ModelBackend):
#     def authenticate(self, request, username=None, password=None, **kwargs):
#         if username is None:
#             username = kwargs.get(User.USERNAME_FIELD)
#         if username is None or password is None:
#             return
#         try:
#             user = User.objects.get(
#                 Q(username__exact=username) |
#                 Q(email__exact=username)
#             )
#             if user.check_password(password) and self.user_can_authenticate(user):
#                 return user
#         except:
#             return None

class SafeJWTAuthentication(BaseAuthentication):
    """
    JWT Authentication
    헤더의 jwt 값을 디코딩해 얻은 user_id 값을 통해서 유저 인증 여부를 판단한다.
    """
    
    def authenticate(self, request):
        authorization_header = request.headers.get('Authorization')
        
        if not authorization_header:
            return None
            
        try:
            prefix = authorization_header.split(' ')[0]
            if prefix.lower() != 'jwt':
                raise exceptions.AuthenticationFailed('Token is not jwt')

            access_token = authorization_header.split(' ')[1]
            payload = jwt.decode(
                access_token, settings.SECRET_KEY, algorithms=['HS256']
            )
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('access_token expired')
        except IndexError:
            raise exceptions.AuthenticationFailed('Token prefix missing')
        
        return self.authenticate_credentials(request, payload['user_id'])
    
    def authenticate_credentials(self, request, key):
        user = User.objects.filter(id=key).first()
        
        if user is None:
            raise exceptions.AuthenticationFailed('User not found')
        
        if not user.is_active:
            raise exceptions.AuthenticationFailed('User is inactive')
        
        self.enforce_csrf(request)
        return (user, None)

    def enforce_csrf(self, request):
        check = CSRFCheck()
        
        check.process_request(request)
        reason = check.process_view(request, None, (), {})
        if reason:
            raise exceptions.PermissionDenied(f'CSRF Failed: {reason}')