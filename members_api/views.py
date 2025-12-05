import jwt
from django.conf import settings
from django.contrib.auth import get_user_model, authenticate
from rest_framework import viewsets, status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from courses_app.models import Course
from members_api.serializers import CourseSerializer, MemberSerializer, RefreshTokenSerializer, LoginSerializer
from members_api.utils import create_access_token, create_refresh_token

User = get_user_model()


class MembersViewSet(viewsets.ModelViewSet):
    serializer_class = MemberSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['first_name', 'last_name', 'email', 'phone']
    ordering_fields = ['date_joined', 'last_login']


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['start_date', 'end_date']


class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        user = authenticate(
            username=request.data.get('phone'),
            password=request.data.get('password')
        )
        if not user:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({
            'access_token': create_access_token(user),
            'refresh_token': create_refresh_token(user)
        })


class RefreshTokenView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RefreshTokenSerializer

    def post(self, request):
        token = request.data.get('refresh_token')
        if not token:
            return Response({'error': 'Refresh token required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            if not payload.get('token_type') == 'refresh':
                raise AuthenticationFailed('Invalid token type')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')

        if not payload:
            return Response({'error': 'Invalid or expired refresh token'}, status=status.HTTP_401_UNAUTHORIZED)

        user = User.objects.filter(id=payload.get('id')).first()
        if not user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        return Response({
            'access_token': create_access_token(user)
        })
