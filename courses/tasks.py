from pathlib import Path

from celery import shared_task
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.db.models import Avg, Count, Q
from django.http import QueryDict
from django.utils import timezone

from .models import Course
from .serializers import CourseSerializer
from .services import (
    PUBLIC_COURSE_CACHE_TIMEOUT,
    public_course_detail_cache_key,
    public_course_list_cache_key,
)


class _AnonymousRequest:
    user = AnonymousUser()


def _serialize_public_courses(queryset):
    serializer = CourseSerializer(
        queryset,
        many=True,
        context={'request': _AnonymousRequest()}
    )
    return serializer.data


@shared_task
def warm_public_course_cache():
    queryset = Course.objects.select_related('instructor').annotate(
        average_rating=Avg('ratings__score')
    ).filter(status='published').order_by('-created_at')

    payload = {
        'count': queryset.count(),
        'next': None,
        'previous': None,
        'results': _serialize_public_courses(queryset),
    }
    cache_key = public_course_list_cache_key(QueryDict('', mutable=False))
    from django.core.cache import cache
    cache.set(cache_key, payload, timeout=PUBLIC_COURSE_CACHE_TIMEOUT)

    warmed_detail_count = 0
    for course in queryset:
        detail_payload = CourseSerializer(
            course,
            context={'request': _AnonymousRequest()}
        ).data
        cache.set(
            public_course_detail_cache_key(course.id),
            detail_payload,
            timeout=PUBLIC_COURSE_CACHE_TIMEOUT,
        )
        warmed_detail_count += 1

    return {
        'warmed_list': True,
        'warmed_detail_count': warmed_detail_count,
        'timestamp': timezone.now().isoformat(),
    }


@shared_task
def generate_course_report_snapshot():
    report_dir = Path(settings.MEDIA_ROOT) / 'reports'
    report_dir.mkdir(parents=True, exist_ok=True)
    timestamp = timezone.now()
    report_path = report_dir / f'course-report-{timestamp.strftime("%Y%m%d-%H%M%S")}.txt'

    summary = Course.objects.aggregate(
        total_courses=Count('id'),
        published_courses=Count('id', filter=Q(status='published')),
        draft_courses=Count('id', filter=Q(status='draft')),
        archived_courses=Count('id', filter=Q(status='archived')),
        total_ratings=Count('ratings'),
    )

    lines = [
        'Simple LMS Course Report Snapshot',
        f'Generated at: {timestamp.isoformat()}',
        f"Total courses: {summary['total_courses']}",
        f"Published courses: {summary['published_courses']}",
        f"Draft courses: {summary['draft_courses']}",
        f"Archived courses: {summary['archived_courses']}",
        f"Total ratings: {summary['total_ratings']}",
        '',
        'Published course details:',
    ]

    published_courses = Course.objects.select_related('instructor').annotate(
        rating_average=Avg('ratings__score'),
        enrollment_total=Count('enrollments'),
        lesson_total=Count('lessons'),
    ).filter(status='published').order_by('title')

    for course in published_courses:
        lines.append(
            f"- {course.title} | instructor={course.instructor.username} | "
            f"lessons={course.lesson_total} | enrollments={course.enrollment_total} | "
            f"average_rating={round(course.rating_average or 0, 1)}"
        )

    report_path.write_text('\n'.join(lines), encoding='utf-8')
    return str(report_path)
