from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Course, Enrollment, Lesson, LessonProgress

User = get_user_model()


class CourseWorkflowTests(APITestCase):
    def setUp(self):
        self.instructor = User.objects.create_user(
            username='instructor_test',
            password='password123',
            role='instructor'
        )
        self.student = User.objects.create_user(
            username='student_test',
            password='password123',
            role='student'
        )
        self.other_student = User.objects.create_user(
            username='student_other',
            password='password123',
            role='student'
        )
        self.course = Course.objects.create(
            title='Python Dasar',
            description='Belajar Python',
            instructor=self.instructor,
            category='Programming',
            level='Beginner',
            status='published'
        )
        self.lesson = Lesson.objects.create(
            course=self.course,
            title='Intro',
            content='Materi intro',
            order=1
        )
        Enrollment.objects.create(user=self.student, course=self.course)

    def authenticate(self, user, password='password123'):
        response = self.client.post(
            '/api/token/',
            {'username': user.username, 'password': password},
            format='json'
        )
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_student_only_sees_enrolled_lessons(self):
        self.authenticate(self.other_student)
        response = self.client.get('/api/lessons/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_student_can_create_enrollment_from_endpoint(self):
        self.authenticate(self.other_student)
        response = self.client.post(
            '/api/enrollments/',
            {'course_id': self.course.id},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Enrollment.objects.filter(user=self.other_student, course=self.course).exists()
        )

    def test_student_cannot_create_lesson(self):
        self.authenticate(self.student)
        response = self.client.post(
            '/api/lessons/',
            {
                'course': self.course.id,
                'title': 'Lesson Baru',
                'content': 'Isi lesson',
                'order': 2,
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_student_can_create_progress_for_enrolled_lesson(self):
        self.authenticate(self.student)
        response = self.client.post(
            '/api/lesson-progress/',
            {'lesson_id': self.lesson.id, 'completed': True},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        progress = LessonProgress.objects.get(user=self.student, lesson=self.lesson)
        self.assertTrue(progress.completed)
        self.assertIsNotNone(progress.completed_at)

    def test_student_cannot_create_progress_for_unenrolled_lesson(self):
        self.authenticate(self.other_student)
        response = self.client.post(
            '/api/lesson-progress/',
            {'lesson_id': self.lesson.id, 'completed': True},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
