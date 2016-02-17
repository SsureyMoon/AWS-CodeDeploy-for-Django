from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'date_joined', 'is_active',
                  'profile_img_url',)


class CreateUserSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(max_length=75, required=True,
                                  validators=[UniqueValidator(queryset=User.objects.all())])

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password',)
        write_only_fields = ('password',)