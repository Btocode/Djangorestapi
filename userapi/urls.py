from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from django.urls import path
from .views import UserDetailAPI,RegisterUserAPIView, LoginView, IndividualUserDetailAPI, LogoutView, MyTokenObtainPairView

urlpatterns = [
  path('v1/details',UserDetailAPI.as_view()),
  path('v1/signup',RegisterUserAPIView.as_view()),

  # JWT Cookies authentication
  path('v1/login',LoginView.as_view()),
  path('v1/getuser',IndividualUserDetailAPI.as_view()),
  path('v1/logout',LogoutView.as_view()),

  #JWT Token authentication 
  path('v1/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
  path('v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]