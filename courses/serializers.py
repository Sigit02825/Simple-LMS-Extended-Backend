from rest_framework import serializers
from django.db.models import Avg
from .models import Course, Lesson, Enrollment, LessonProgress, Rating, Wishlist
from users.serializers import UserSerializer


class CourseSerializer(serializers.ModelSerializer):
    instructor = UserSerializer(read_only=True)
    average_rating = serializers.SerializerMethodField()
    rating_count = serializers.SerializerMethodField()
    is_wishlisted = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'description', 'instructor', 'created_at', 'updated_at',
            'category', 'level', 'status', 'average_rating', 'rating_count', 'is_wishlisted'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'instructor']

    def get_average_rating(self, obj):
        avg = obj.ratings.aggregate(Avg('score'))['score__avg']
        return round(avg, 1) if avg else 0

    def get_rating_count(self, obj):
        return obj.ratings.count()

    def get_is_wishlisted(self, obj):
        user = self.context.get('request').user
        if user and user.is_authenticated:
            return obj.wishlisted_by.filter(user=user).exists()
        return False


class LessonSerializer(serializers.ModelSerializer):
    is_completed = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ['id', 'course', 'title', 'content', 'order', 'created_at', 'is_completed']
        read_only_fields = ['id', 'created_at']

    def get_is_completed(self, obj):
        user = self.context.get('request').user
        if user and user.is_authenticated:
            return obj.progress.filter(user=user, completed=True).exists()
        return False


class EnrollmentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    course_id = serializers.PrimaryKeyRelatedField(
        source='course',
        queryset=Course.objects.filter(status='published'),
        write_only=True
    )
    progress_percentage = serializers.SerializerMethodField()

    class Meta:
        model = Enrollment
        fields = ['id', 'user', 'course', 'course_id', 'enrolled_at', 'completed_at', 'progress_percentage']
        read_only_fields = ['id', 'enrolled_at', 'user']

    def get_progress_percentage(self, obj):
        total_lessons = obj.course.lessons.count()
        if total_lessons == 0:
            return 0
        completed_lessons = LessonProgress.objects.filter(
            user=obj.user, lesson__course=obj.course, completed=True
        ).count()
        return round((completed_lessons / total_lessons) * 100, 1)


class LessonProgressSerializer(serializers.ModelSerializer):
    lesson = serializers.PrimaryKeyRelatedField(read_only=True)
    lesson_id = serializers.PrimaryKeyRelatedField(
        source='lesson',
        queryset=Lesson.objects.all(),
        write_only=True
    )

    class Meta:
        model = LessonProgress
        fields = ['id', 'user', 'lesson', 'lesson_id', 'completed', 'completed_at']
        read_only_fields = ['id', 'user', 'completed_at']


class RatingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    course = serializers.PrimaryKeyRelatedField(read_only=True)
    course_id = serializers.PrimaryKeyRelatedField(
        source='course',
        queryset=Course.objects.filter(status='published'),
        write_only=True
    )

    class Meta:
        model = Rating
        fields = ['id', 'user', 'course', 'course_id', 'score', 'comment', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


class WishlistSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    course_id = serializers.PrimaryKeyRelatedField(
        source='course',
        queryset=Course.objects.filter(status='published'),
        write_only=True
    )

    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'course', 'course_id', 'added_at']
        read_only_fields = ['id', 'user', 'added_at']
