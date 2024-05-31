from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
import random
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.serializers import Serializer
from .models import User
from .serializers import UserSerializer, UserLoginSerializer, ResetPasswordSerializer, ResetPasswordVerifySerializer, \
    LogoutSerializer, UserProfileSerializer


class RegistrationAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = serializer.save()

            # Sending activation email
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            activation_link = request.build_absolute_uri(
                reverse('activate', kwargs={'uid': uid, 'token': token})
            )

            message = (
                f"<h1>Здравствуйте, {user.email}!</h1>"
                f"<p>Спасибо за регистрацию на нашем сайте. Пожалуйста, перейдите по ссылке ниже, чтобы активировать ваш аккаунт:</p>"
                f"<p><a href='{activation_link}'>Активировать аккаунт</a></p>"
                f"<p>Если ссылка не работает, скопируйте и вставьте следующий URL в ваш браузер:</p>"
                f"<p>{activation_link}</p>"
                f"<p>С наилучшими пожеланиями,<br>Команда {settings.BASE_URL}</p>"
            )

            send_mail(
                _('Активация вашего аккаунта'),
                '',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
                html_message=message,
            )

            return Response({
                'response': True,
                'message': _('Пользователь успешно зарегистрирован. Пожалуйста, проверьте вашу электронную почту для инструкций по активации.')
            }, status=status.HTTP_201_CREATED)

        except IntegrityError:
            return Response({
                'response': False,
                'message': _('Не удалось зарегистрировать пользователя')
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ActivateUserView(generics.GenericAPIView):
    serializer_class = Serializer  # Adding an empty serializer

    def get(self, request, uid, token):
        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)
            if default_token_generator.check_token(user, token):
                user.is_verified = True
                user.save()
                return Response({
                    'response': True,
                    'message': _('Аккаунт успешно активирован')
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'response': False,
                    'message': _('Неверный или истекший токен')
                }, status=status.HTTP_400_BAD_REQUEST)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({
                'response': False,
                'message': _('Недействительная ссылка активации')
            }, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            token, created = Token.objects.get_or_create(user=request.user)
            return Response({
                'response': True,
                'token': token.key
            }, status=status.HTTP_200_OK)
        else:
            serializer = UserLoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request, email=email, password=password)

            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'response': True,
                    'token': token.key
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'response': False,
                    'message': _('Неверные учетные данные')
                }, status=status.HTTP_401_UNAUTHORIZED)

class ResetPasswordView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        try:
            user = User.objects.get(email=email)
            new_password = str(random.randint(1000, 9999))
            user.set_password(new_password)
            user.save()

            message = f'Ваш новый пароль: {new_password}. Пожалуйста, измените его после входа в систему.'

            send_mail(
                _('Сброс пароля'),
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )

            return Response({
                'response': True,
                'message': _('Пароль сброшен. Проверьте вашу электронную почту для получения инструкций.')
            })

        except User.DoesNotExist:
            return Response({
                'response': False,
                'message': _('Пользователь с этим адресом электронной почты не существует.')
            }, status=status.HTTP_404_NOT_FOUND)

class ResetPasswordVerifyView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ResetPasswordVerifySerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email")
        new_password = serializer.validated_data.get("new_password")

        try:
            user = User.objects.get(email=email)

            user.set_password(new_password)
            user.save()

            return Response({
                'response': True,
                'message': _('Пароль успешно изменен.')
            }, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({
                'response': False,
                'message': _('Пользователь с этим адресом электронной почты не найден.')
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'response': False,
                'message': _('Ошибка при сбросе пароля.')
            }, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({
            'response': True,
            'message': _('Вы успешно вышли из системы.')
        })
class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user