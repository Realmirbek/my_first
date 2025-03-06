from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .serializers import (
    UserRegistrationSerializer,
    MyTokenObtainPairSerializer,
    PasswordResetRequestSerializer, PasswordSetSerializer, UserListSerializer, UserDetailSerializer

)

User = get_user_model()

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class PasswordResetRequestView(APIView):
    @swagger_auto_schema(
        request_body=PasswordResetRequestSerializer,
        responses={200: openapi.Response("Ссылка для сброса пароля отправлена")}
    )
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.send_reset_email()
            return Response({"message": "Ссылка для сброса пароля отправлена на email."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class PasswordSetView(APIView):
    @swagger_auto_schema(
        request_body=PasswordSetSerializer,
        responses={200: openapi.Response("Пароль успешно изменен")}
    )
    def post(self, request):
        serializer = PasswordSetSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"message": "Пароль успешно изменен."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDeleteView(APIView):


    @swagger_auto_schema(
        operation_description="Удалить пользователя по ID",
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="ID пользователя", type=openapi.TYPE_INTEGER)
        ],
        responses={204: "Пользователь удален", 404: "Пользователь не найден"}
    )
    def delete(self, request, id):
        try:
            user = User.objects.get(id=id)
            user.delete()
            return Response({"message": "Пользователь удален"}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({"error": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = []  # Убираем требование авторизации

    @swagger_auto_schema(
        operation_description="Получить список всех пользователей",
        responses={200: UserListSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = []  # Делаем публичным, если не нужна авторизация

    @swagger_auto_schema(
        operation_description="Получить данные пользователя по ID",
        responses={200: UserDetailSerializer()}
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
