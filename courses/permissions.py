from rest_framework import permissions


class IsCourseInstructorOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_authenticated and request.user.role == 'admin':
            return True
        course = getattr(obj, 'course', obj)
        return getattr(course, 'instructor', None) == request.user


class IsEnrolledOrInstructorOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_authenticated:
            course = getattr(obj, 'course', obj)
            if request.user.role == 'admin' or getattr(course, 'instructor', None) == request.user:
                return True
            return course.enrollments.filter(user=request.user).exists()
        return False


class IsEnrollmentOwnerInstructorOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.role == 'admin':
            return True
        if request.user.role == 'instructor':
            return obj.course.instructor == request.user
        return obj.user == request.user


class IsProgressOwnerInstructorOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.role == 'admin':
            return True
        if request.user.role == 'instructor':
            return obj.lesson.course.instructor == request.user
        return obj.user == request.user
