
from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.status import *
from rest_framework.response import Response

from authentication.models.base import Profile


class UserListCreateAPIView(APIView):
    class UserSerializer(serializers.ModelSerializer):
        class ProfileSerializer(serializers.ModelSerializer):
            class Meta:
                model = Profile
                fields = ('gender', 'phone', 'age', 'address', 'birthday', 'avatar')
        profile = ProfileSerializer(read_only=True,)
        password = serializers.CharField(write_only=True, required=True,)
        class Meta:
            model = get_user_model()
            fields = ('username', 'password', 'email', 'profile')
        def create(self, validated_data):   # TODO
            password = validated_data.pop("password")
            user = super().create(validated_data)
            user.set_password(password)
            user.save()
            return user

    def get(self, request, format=None):
        users = get_user_model().objects.all()
        serializer = self.UserSerializer(users, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    def post(self, request, format=None):
        serializer = self.UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    



class UserRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = '__all__'




