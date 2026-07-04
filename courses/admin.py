from django.contrib import admin
from .models import (
    Course, Lesson, Enrollment, LessonProgress, Rating, Wishlist
)


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1


class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline]
    list_display = ('title', 'instructor', 'category', 'level', 'status', 'created_at')
    list_filter = ('status', 'category', 'level', 'created_at')
    search_fields = ('title', 'description')


class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'enrolled_at', 'completed_at')
    list_filter = ('enrolled_at', 'completed_at')


class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'completed', 'completed_at')
    list_filter = ('completed', 'completed_at')


class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'score', 'created_at')
    list_filter = ('score', 'created_at')


class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'added_at')
    list_filter = ('added_at',)


admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson)
admin.site.register(Enrollment, EnrollmentAdmin)
admin.site.register(LessonProgress, LessonProgressAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Wishlist, WishlistAdmin)
