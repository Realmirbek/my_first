from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from urllib.parse import urlencode
from django.contrib.auth.password_validation import validate_password

from django.core.exceptions import ValidationError

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def validate_password(self, value):  # ✅ Исправленный метод валидации пароля
        try:

            validate_password(value)  # Встроенный валидатор Django
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)  # ✅ Возвращаем список ошибок
        return value  # ✅ Если ошибок нет, возвращаем пароль

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Пользователь с таким email не найден.")
        return value

    def send_reset_email(self):
        email = self.validated_data['email']
        reset_url = f"http://127.0.0.1:8000/polls/set-new-password/?{urlencode({'email': email})}"

        send_mail(
            "Сброс пароля",
            f"Привет! Перейди по этой ссылке, чтобы установить новый пароль: {reset_url} "
            f"Если ты не запрашивал сброс пароля, проигнорируй это письмо.",
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )

class PasswordSetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    new_password = serializers.CharField(write_only=True)

    def validate_new_password(self, value):  # ✅ Исправленная валидация нового пароля
        try:
            validate_password(value)

        except ValidationError as e:
            raise serializers.ValidationError(e.messages)  # ✅ Возвращаем ошибки корректно
        return value

    def validate(self, data):
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            raise serializers.ValidationError("Пользователь с таким email не найден.")

        user.set_password(data['new_password'])
        user.save()
        return data


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')  # Добавь нужные поля



class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')  # Можно добавить другие нужные поля

