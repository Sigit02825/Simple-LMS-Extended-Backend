from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class UserRegistrationTests(APITestCase):
    def test_public_registration_forces_student_role(self):
        response = self.client.post(
            '/api/users/',
            {
                'username': 'new_user',
                'email': 'new@example.com',
                'password': 'password123',
                'role': 'admin',
            },
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(username='new_user')
        self.assertEqual(user.role, 'student')
