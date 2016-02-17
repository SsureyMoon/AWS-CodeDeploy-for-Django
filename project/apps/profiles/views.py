from django.utils import importlib
from django.conf import settings
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import api_view, permission_classes, parser_classes, authentication_classes
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .serializers import UserSerializer, CreateUserSerializer
from .models import User

from authentication.utils import create_jwt_token


module = settings.DELETE_MEDIA_FILE_METHOD.split('.')
func = module.pop()
delete_media_method = getattr(importlib.import_module('.'.join(module)), func)


class ProfileView(APIView):

    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user
        user_data = UserSerializer(user).data

        return Response(dict(user=user_data), status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = UserSerializer(user)

        data = serializer.data

        return Response(data)


class UserViewSet(mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    """
    Creates, Updates, and retrieves User accounts
    """
    authentication_classes = (JSONWebTokenAuthentication,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny,]

    def create(self, request, *args, **kwargs):

        if not all([request.data.get('username'), request.data.get('password')]):
            raise ValidationError(detail="username or password is not provided.")

        serializer = CreateUserSerializer(data=request.data)

        if not serializer.is_valid():
            for key in serializer.errors:
                print key
                for error in serializer.errors[key]:
                    print error
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # create user
        user = serializer.save()
        user_data = UserSerializer(user).data

        data = {
            "user": user_data,
            "token": create_jwt_token(user),
        }
        return Response(data, status=status.HTTP_201_CREATED)

    def validate_request_data(self, request):
        data = dict(request.data)
        if data.get('password') == data.get('confirm'):
            del data['confirm']
            return data
        return Response(serializers.ValidationError("Passwords do not match"), status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST',])
@permission_classes([IsAuthenticated,])
@authentication_classes([JSONWebTokenAuthentication])
@parser_classes([FormParser, MultiPartParser,])
def post_profile_photo(request, format=None, *args, **kwargs):

    user = request.user
    file_obj = request.data.get('file')
    path = None
    if file_obj:
        if user.profile_img:
            path = user.profile_img.path
        print user.profile_img
        user.profile_img = file_obj
        user.save()
        if path:
            delete_media_method(path)

    return Response(status=status.HTTP_204_NO_CONTENT)

