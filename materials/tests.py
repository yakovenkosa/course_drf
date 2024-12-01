from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from materials.models import Course, Lesson, Subscription
from users.models import User

User = get_user_model()


class CourseTestCase(APITestCase):
    """Класс для тестирования курса"""

    def setUp(self) -> None:
        self.user = User.objects.create(email="testuser@example.com", is_active=True)
        self.user.set_password("testpassword")
        self.user.save()

        self.access_token = AccessToken.for_user(self.user)

    def test_create_course(self):
        """Тест для создания курса"""
        data = {"title": "test", "description": "test", "owner": self.user.id}
        response = self.client.post(
            "/course/", data=data, HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertTrue(Course.objects.filter(title="test").exists())
        self.assertEqual(Course.objects.count(), 1)
        self.assertEqual(Course.objects.get().title, "test")


class LessonPlatformTestCase(APITestCase):
    """Класс для проверки корректности работы CRUD уроков и подписки на уроки"""

    def setUp(self) -> None:
        self.user = User.objects.create(email="testuser@example.com", is_active=True)
        self.user.set_password("testpassword")
        self.user.save()

        self.course = Course.objects.create(title="Test Course", description="Test Description", owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_create_lesson(self):
        """Тест для создания урока"""
        data = {
            "title": "Test Lesson",
            "description": "Lesson Description",
            "course": self.course.id,
            "link_to_video": "http://www.youtube.com/2",
            "course": self.course.id,
        }
        response = self.client.post("/lesson/create/", data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_lessons(self):
        """Тест для получения списка уроков"""
        Lesson.objects.create(
            title="Test Lesson 1",
            description="Description 1",
            course=self.course,
            link_to_video="http://www.youtube.com/1",
        )
        Lesson.objects.create(
            title="Test Lesson 2",
            description="Description 2",
            course=self.course,
            link_to_video="http://www.youtube.com/2",
            owner=self.user,
        )

        response = self.client.get("/lesson/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_retrieve_lesson(self):
        """Тест для получения нужного урока"""
        lesson = Lesson.objects.create(
            title="Test Lesson",
            description="Description",
            course=self.course,
            link_to_video="http://www.youtube.com/1",
            owner=self.user,
        )

        response = self.client.get(f"/lesson/{lesson.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test Lesson")

    def test_update_lesson(self):
        """Тест для изменения урока"""
        lesson = Lesson.objects.create(
            title="Test Lesson",
            description="Description",
            course=self.course,
            link_to_video="http://www.youtube.com/1",
            owner=self.user,
        )
        data = {
            "title": "Updated Lesson",
            "description": "Updated Description",
            "course": self.course.id,
            "link_to_video": "http://www.youtube.com/1",
            "owner": self.user.id,
        }

        response = self.client.put(
            f"/lesson/update/{lesson.id}/",
            data=data,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        lesson.refresh_from_db()
        self.assertEqual(lesson.title, "Updated Lesson")

    def test_delete_lesson(self):
        """Тест для удаления урока"""
        lesson = Lesson.objects.create(
            title="Test Lesson",
            description="Description",
            course=self.course,
            link_to_video="http://www.youtube.com/1",
            owner=self.user,
        )

        response = self.client.delete(f"/lesson/delete/{lesson.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.filter(id=lesson.id).exists())

    def test_subscription(self):
        """Тест подписки на обновление курса"""
        response = self.client.post("/subscription/", {"course_id": self.course.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )
