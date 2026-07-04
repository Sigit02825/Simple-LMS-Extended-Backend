from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import UserViewSet, LogoutView, CustomTokenObtainPairView, CustomTokenRefreshView

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'logout', LogoutView, basename='logout')

urlpatterns = [
    path('', include(router.urls)),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
]
