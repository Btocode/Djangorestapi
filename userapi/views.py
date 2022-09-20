from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer,RegisterSerializer
from custom_user.models import CustomUser
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics
from rest_framework.exceptions import AuthenticationFailed

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

    return Response({
      "message": "Authentication Successful",
    })