from django.urls import path
from .views import UserDetailAPI,RegisterUserAPIView
urlpatterns = [
  path('v1/details',UserDetailAPI.as_view()),
  path('v1/signup',RegisterUserAPIView.as_view()),
]