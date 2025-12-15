from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework.routers import DefaultRouter

from members_api.views import MembersViewSet, CourseViewSet, LoginView, RefreshTokenView

router = DefaultRouter()
router.register(r'members', MembersViewSet)
router.register(r'courses', CourseViewSet, basename='courses-api')

urlpatterns = [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('', include(router.urls)),
    path('token/', LoginView.as_view(), name='token'),
    path('refresh/', RefreshTokenView.as_view(), name='refresh'),
]
