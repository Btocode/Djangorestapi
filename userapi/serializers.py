from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from custom_user.models import CustomUser

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = CustomUser
    fields = ["first_name", "last_name", 'email', 'phone', 'types', 'address' ]

#Serializer to Register User
class RegisterSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(
    required=True,
    validators=[UniqueValidator(queryset=CustomUser.objects.all())]
  )
  password = serializers.CharField(
    write_only=True, required=True, validators=[validate_password])
  password2 = serializers.CharField(write_only=True, required=True)
  class Meta:
    model = CustomUser
    fields = ["first_name", "last_name", 'email', 'password', 'password2', 'phone', 'types', 'address' ]
    extra_kwargs = {
      'first_name': {'required': True},
      'last_name': {'required': True}
    }
  def validate(self, attrs):
    if attrs['password'] != attrs['password2']:
      raise serializers.ValidationError(
        {"password": "Password fields didn't match."})
    return attrs
  def create(self, validated_data):
    user = CustomUser.objects.create(
      email=validated_data['email'],
      first_name=validated_data['first_name'],
      last_name=validated_data['last_name'],
      phone=validated_data['phone'],
      types=validated_data['types'],
      address=validated_data['address'],
    )
    user.set_password(validated_data['password'])
    user.save()
    return user
