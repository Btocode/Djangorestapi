from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer,RegisterSerializer
from custom_user.models import CustomUser
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


import jwt, datetime


# Class based view to Get User Details using Token Authentication


class UserDetailAPI(APIView):
  authentication_classes = (TokenAuthentication,)
  permission_classes = (AllowAny,)
  def get(self,request,*args,**kwargs):
    user = CustomUser.objects.all()
    serializer = UserSerializer(user, many = True)
    return Response(serializer.data)

#Class based view to register user
class RegisterUserAPIView(generics.CreateAPIView):
  permission_classes = (AllowAny,)
  serializer_class = RegisterSerializer


class LoginView(APIView):
  def post(self, request, *args,**kwargs):
    email = request.data.get('email')
    password = request.data.get('password')


    user = CustomUser.objects.filter(email=email).first()

    if user is None:
      raise AuthenticationFailed('User not found!')

    if not user.check_password(password):
      raise AuthenticationFailed('Incorrect password!')

    payload = {
      'id': user.email,
      'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=1),
      'iat': datetime.datetime.utcnow()
    }
    token = jwt.encode(payload, 'secret', algorithm='HS256')

    response = Response()

    response.set_cookie(key='jwt', value=token, httponly=True)
    response.data = {
      "jwt": token,
    }

    return response;

class IndividualUserDetailAPI(APIView):
  authentication_classes = (TokenAuthentication,)
  permission_classes = (AllowAny,)
  def get(self,request,*args,**kwargs):
    token = request.COOKIES.get('jwt')
    if not token:
      raise AuthenticationFailed('User is not Authenticated')
    try:
      payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
      raise AuthenticationFailed('Unauthenticated')
    user = CustomUser.objects.filter(email = payload['id']).first()
    serializer = UserSerializer(user)
    return Response(serializer.data)

class LogoutView(APIView):
  def post(self, request, *args,**kwargs):
    response = Response()
    response.delete_cookie('jwt')
    response.data = {
      "message": "Successfully logged out"
    }
    return response