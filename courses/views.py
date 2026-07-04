from django.utils import timezone
from django.db.models import Avg, Q
from django.core.cache import cache
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .models import Course, Lesson, Enrollment, LessonProgress, Rating, Wishlist
from .serializers import (
    CourseSerializer, LessonSerializer, EnrollmentSerializer,
    LessonProgressSerializer, RatingSerializer, WishlistSerializer
)
from .permissions import (
    IsCourseInstructorOrAdmin,
    IsEnrolledOrInstructorOrAdmin,
    IsEnrollmentOwnerInstructorOrAdmin,
    IsProgressOwnerInstructorOrAdmin,
)
from .services import (
    PUBLIC_COURSE_CACHE_TIMEOUT,
    public_course_list_cache_key,
    public_course_detail_cache_key,
    invalidate_public_course_cache,
)
from users.permissions import IsAdminOrInstructor, IsStudent


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'level', 'status', 'instructor']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'title', 'average_rating']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        elif self.action in ['create']:
            return [IsAdminOrInstructor()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsCourseInstructorOrAdmin()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        queryset = Course.objects.select_related('instructor').annotate(
            average_rating=Avg('ratings__score')
        ).order_by('-created_at')
        user = self.request.user
        if not user.is_authenticated:
            return queryset.filter(status='published')
        if hasattr(user, 'role') and user.role == 'admin':
            return queryset
        if hasattr(user, 'role') and user.role == 'instructor':
            if self.action in ['list', 'retrieve']:
                return queryset.filter(Q(status='published') | Q(instructor=user)).distinct()
            return queryset.filter(instructor=user)
        return queryset.filter(status='published')

    def list(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().list(request, *args, **kwargs)

        cache_key = public_course_list_cache_key(request.query_params)
        cached_payload = cache.get(cache_key)
        if cached_payload is not None:
            return Response(cached_payload)

        response = super().list(request, *args, **kwargs)
        if response.status_code == 200:
            cache.set(cache_key, response.data, timeout=PUBLIC_COURSE_CACHE_TIMEOUT)
        return response

    def retrieve(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().retrieve(request, *args, **kwargs)

        cache_key = public_course_detail_cache_key(kwargs['pk'])
        cached_payload = cache.get(cache_key)
        if cached_payload is not None:
            return Response(cached_payload)

        response = super().retrieve(request, *args, **kwargs)
        if response.status_code == 200:
            cache.set(cache_key, response.data, timeout=PUBLIC_COURSE_CACHE_TIMEOUT)
        return response

    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)
        invalidate_public_course_cache()

    def perform_update(self, serializer):
        course = serializer.save()
        invalidate_public_course_cache(course.id)

    def perform_destroy(self, instance):
        course_id = instance.id
        instance.delete()
        invalidate_public_course_cache(course_id)

    @action(detail=True, methods=['post'], permission_classes=[IsStudent()])
    def enroll(self, request, pk=None):
        course = self.get_object()
        enrollment, created = Enrollment.objects.get_or_create(
            user=request.user, course=course
        )
        serializer = EnrollmentSerializer(enrollment)
        return Response(serializer.data)


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.select_related('course', 'course__instructor').all()
    serializer_class = LessonSerializer

    def get_queryset(self):
        queryset = Lesson.objects.select_related('course', 'course__instructor')
        user = self.request.user
        if not user.is_authenticated:
            return Lesson.objects.none()
        if user.role == 'admin':
            return queryset
        if user.role == 'instructor':
            return queryset.filter(Q(course__status='published') | Q(course__instructor=user)).distinct()
        enrolled_course_ids = Enrollment.objects.filter(user=user).values_list('course_id', flat=True)
        return queryset.filter(course__status='published', course_id__in=enrolled_course_ids)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            if self.action == 'create':
                return [IsAdminOrInstructor()]
            return [IsCourseInstructorOrAdmin()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        course = serializer.validated_data['course']
        if self.request.user.role == 'instructor' and course.instructor != self.request.user:
            raise PermissionDenied('Instructor hanya boleh menambah lesson pada course miliknya sendiri.')
        serializer.save()

    @action(detail=True, methods=['post'], permission_classes=[IsStudent()])
    def complete(self, request, pk=None):
        lesson = self.get_object()
        progress, created = LessonProgress.objects.get_or_create(
            user=request.user, lesson=lesson
        )
        if not progress.completed:
            progress.completed = True
            progress.completed_at = timezone.now()
            progress.save()
        serializer = LessonProgressSerializer(progress)
        return Response(serializer.data)


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Enrollment.objects.none()
        if hasattr(user, 'role') and user.role == 'admin':
            return Enrollment.objects.all()
        elif hasattr(user, 'role') and user.role == 'instructor':
            return Enrollment.objects.filter(course__instructor=user)
        return Enrollment.objects.filter(user=user)

    def get_permissions(self):
        if self.action == 'create':
            return [IsStudent()]
        if self.action in ['update', 'partial_update', 'destroy', 'retrieve']:
            return [permissions.IsAuthenticated(), IsEnrollmentOwnerInstructorOrAdmin()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LessonProgressViewSet(viewsets.ModelViewSet):
    queryset = LessonProgress.objects.all()
    serializer_class = LessonProgressSerializer

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return LessonProgress.objects.none()
        if hasattr(user, 'role') and user.role == 'admin':
            return LessonProgress.objects.select_related('lesson', 'lesson__course', 'user')
        if hasattr(user, 'role') and user.role == 'instructor':
            return LessonProgress.objects.select_related('lesson', 'lesson__course', 'user').filter(
                lesson__course__instructor=user
            )
        return LessonProgress.objects.select_related('lesson', 'lesson__course', 'user').filter(user=user)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsStudent()]
        if self.action in ['retrieve']:
            return [permissions.IsAuthenticated(), IsProgressOwnerInstructorOrAdmin()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        lesson = serializer.validated_data['lesson']
        if not Enrollment.objects.filter(user=self.request.user, course=lesson.course).exists():
            raise PermissionDenied('Student harus terdaftar pada course sebelum membuat progress.')
        progress = serializer.save(user=self.request.user)
        if progress.completed and not progress.completed_at:
            progress.completed_at = timezone.now()
            progress.save(update_fields=['completed_at'])

    def perform_update(self, serializer):
        progress = serializer.save()
        if progress.completed and not progress.completed_at:
            progress.completed_at = timezone.now()
            progress.save(update_fields=['completed_at'])
        elif not progress.completed and progress.completed_at:
            progress.completed_at = None
            progress.save(update_fields=['completed_at'])


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Rating.objects.none()
        if hasattr(user, 'role') and user.role == 'admin':
            return Rating.objects.all()
        return Rating.objects.filter(user=user)

    def perform_create(self, serializer):
        rating = serializer.save(user=self.request.user)
        invalidate_public_course_cache(rating.course_id)

    def perform_update(self, serializer):
        rating = serializer.save()
        invalidate_public_course_cache(rating.course_id)

    def perform_destroy(self, instance):
        course_id = instance.course_id
        instance.delete()
        invalidate_public_course_cache(course_id)


class WishlistViewSet(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Wishlist.objects.none()
        return Wishlist.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
