from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Refbook, RefbookElement, RefbookVersion


class RefbookAPITestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
        Этот метод запускается один раз для класса тестов.
        Мы создаем тестовые данные, которые будем использовать в тестах.
        """
        cls.user = User.objects.create_user(username="testuser", password="password")
        cls.refbook = Refbook.objects.create(code="RB1", name="Medical Specialties")
        cls.version1 = RefbookVersion.objects.create(refbook=cls.refbook, version="1.0", start_date=date(2022, 1, 1))
        cls.version2 = RefbookVersion.objects.create(refbook=cls.refbook, version="2.0", start_date=date(2023, 1, 1))

        # Создаем элементы для первой версии
        cls.element1_v1 = RefbookElement.objects.create(version=cls.version1, code="1", value="Therapist")
        cls.element2_v1 = RefbookElement.objects.create(version=cls.version1, code="2", value="Orthopedist")

        # Создаем элементы для второй версии (текущая версия)
        cls.element1_v2 = RefbookElement.objects.create(version=cls.version2, code="1", value="Therapist V2")
        cls.element2_v2 = RefbookElement.objects.create(version=cls.version2, code="2", value="Orthopedist V2")

    def setUp(self):
        """
        Этот метод запускается перед каждым тестом. Здесь мы аутентифицируем пользователя.
        """
        self.client.login(username="testuser", password="password")

    def test_get_refbooks(self):
        """
        Тест для проверки получения списка справочников через API с параметром даты.
        """
        response = self.client.get(reverse("refbooks-list"), {"date": "2022-10-01"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["refbooks"]), 1)
        self.assertEqual(response.json()["refbooks"][0]["code"], "RB1")

    def test_get_elements_with_version(self):
        """
        Тест для проверки получения элементов справочника с указанием версии.
        """
        # Указываем версию 1.0 для проверки элементов первой версии
        response = self.client.get(reverse("refbooks-elements", args=[self.refbook.id]), {"version": "1.0"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["elements"]), 2)
        self.assertEqual(response.json()["elements"][0]["code"], "1")
        self.assertEqual(response.json()["elements"][1]["value"], "Orthopedist")

    def test_get_elements_without_version(self):
        """
        Тест для проверки получения элементов справочника без указания версии.
        Должны возвращаться элементы текущей версии (по самой поздней дате начала).
        """
        # Проверяем элементы текущей версии (версия 2.0, start_date = 2023-01-01)
        response = self.client.get(reverse("refbooks-elements", args=[self.refbook.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["elements"]), 2)
        self.assertEqual(response.json()["elements"][0]["code"], "1")
        self.assertEqual(response.json()["elements"][0]["value"], "Therapist V2")
        self.assertEqual(response.json()["elements"][1]["code"], "2")
        self.assertEqual(response.json()["elements"][1]["value"], "Orthopedist V2")

    def test_check_element_valid_with_version(self):
        """
        Тест для проверки валидации элемента справочника с указанием версии (корректный элемент).
        """
        response = self.client.get(
            reverse("check-element", args=[self.refbook.id]), {"code": "1", "value": "Therapist", "version": "1.0"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["valid"])

    def test_check_element_invalid_with_version(self):
        """
        Тест для проверки валидации элемента справочника с указанием версии (некорректный элемент).
        """
        response = self.client.get(
            reverse("check-element", args=[self.refbook.id]), {"code": "1", "value": "Unknown", "version": "1.0"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()["valid"])

    def test_check_element_valid_without_version(self):
        """
        Тест для проверки валидации элемента справочника, когда версия не указана.
        Элемент должен проверяться в самой последней версии (по дате начала), не позже текущей даты.
        """
        # Элемент существует в версии 2.0 (которая является текущей версией, так как start_date = 2023-01-01)
        response = self.client.get(
            reverse("check-element", args=[self.refbook.id]), {"code": "1", "value": "Therapist V2"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["valid"])

    def test_check_element_invalid_without_version(self):
        """
        Тест для проверки валидации элемента справочника, когда версия не указана.
        Элемент не существует в текущей версии (версия 2.0).
        """
        # Элемент с значением 'Unknown' не существует ни в одной версии
        response = self.client.get(reverse("check-element", args=[self.refbook.id]), {"code": "1", "value": "Unknown"})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()["valid"])
