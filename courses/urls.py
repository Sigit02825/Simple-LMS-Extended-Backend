from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    CourseViewSet, LessonViewSet, EnrollmentViewSet,
    LessonProgressViewSet, RatingViewSet, WishlistViewSet
)

router = DefaultRouter()
router.register(r'courses', CourseViewSet)
router.register(r'lessons', LessonViewSet)
router.register(r'enrollments', EnrollmentViewSet)
router.register(r'lesson-progress', LessonProgressViewSet)
router.register(r'ratings', RatingViewSet)
router.register(r'wishlist', WishlistViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
