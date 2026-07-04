from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from courses.models import Course, Lesson, Enrollment, Rating, Wishlist

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed the database with demo data'

    def upsert_user(self, *, username, email, password, role, is_superuser=False, **extra_fields):
        user, created = User.objects.get_or_create(
            username=username,
            defaults={'email': email, 'role': role, **extra_fields}
        )
        user.email = email
        user.role = role
        for field, value in extra_fields.items():
            setattr(user, field, value)
        user.is_staff = is_superuser or role == 'admin'
        user.is_superuser = is_superuser
        user.set_password(password)
        user.save()
        return user

    def handle(self, *args, **options):
        self.stdout.write('Seeding data...')

        # Create users
        admin_user = self.upsert_user(
            username='admin',
            email='admin@example.com',
            password='admin12345',
            role='admin',
            is_superuser=True
        )
        instructor_user = self.upsert_user(
            username='instructor',
            email='instructor@example.com',
            password='instructor12345',
            role='instructor',
            first_name='John',
            last_name='Doe'
        )
        student_user1 = self.upsert_user(
            username='student1',
            email='student1@example.com',
            password='student12345',
            role='student',
            first_name='Jane',
            last_name='Smith'
        )
        student_user2 = self.upsert_user(
            username='student2',
            email='student2@example.com',
            password='student12345',
            role='student',
            first_name='Bob',
            last_name='Johnson'
        )

        # Create courses
        course1, _ = Course.objects.update_or_create(
            title='Introduction to Python',
            defaults={
                'description': 'Learn the basics of Python programming',
                'instructor': instructor_user,
                'category': 'Programming',
                'level': 'Beginner',
                'status': 'published'
            }
        )
        course2, _ = Course.objects.update_or_create(
            title='Advanced Django',
            defaults={
                'description': 'Master Django framework for web development',
                'instructor': instructor_user,
                'category': 'Web Development',
                'level': 'Advanced',
                'status': 'published'
            }
        )

        # Create lessons
        Lesson.objects.update_or_create(
            course=course1,
            title='Getting Started with Python',
            defaults={
                'content': 'In this lesson, you will learn how to install Python and write your first program.',
                'order': 1
            }
        )
        Lesson.objects.update_or_create(
            course=course1,
            title='Variables and Data Types',
            defaults={
                'content': 'Learn about variables, data types, and basic operations in Python.',
                'order': 2
            }
        )
        Lesson.objects.update_or_create(
            course=course2,
            title='Django Models',
            defaults={
                'content': 'Understand how to define and use Django models.',
                'order': 1
            }
        )
        Lesson.objects.update_or_create(
            course=course2,
            title='Django Views and Templates',
            defaults={
                'content': 'Learn about views, templates, and URL routing in Django.',
                'order': 2
            }
        )

        # Enroll students
        Enrollment.objects.get_or_create(user=student_user1, course=course1)
        Enrollment.objects.get_or_create(user=student_user1, course=course2)
        Enrollment.objects.get_or_create(user=student_user2, course=course1)

        # Add ratings
        Rating.objects.update_or_create(
            user=student_user1,
            course=course1,
            defaults={'score': 5, 'comment': 'Great course!'}
        )
        Rating.objects.update_or_create(
            user=student_user2,
            course=course1,
            defaults={'score': 4, 'comment': 'Very helpful.'}
        )

        # Add to wishlist
        Wishlist.objects.get_or_create(user=student_user2, course=course2)

        self.stdout.write(self.style.SUCCESS('Data seeded successfully!'))
        self.stdout.write(f'Admin: admin / admin12345')
        self.stdout.write(f'Instructor: instructor / instructor12345')
        self.stdout.write(f'Student 1: student1 / student12345')
        self.stdout.write(f'Student 2: student2 / student12345')
