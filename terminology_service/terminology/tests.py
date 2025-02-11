from django.test import TestCase
from django.urls import reverse
from .models import Refbook, RefbookVersion, RefbookElement
from datetime import date

class RefbookAPITestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
        Этот метод запускается один раз для класса тестов. Мы создаем тестовые данные, которые будем использовать в тестах.
        """
        cls.refbook = Refbook.objects.create(code='RB1', name='Medical Specialties')
        cls.version = RefbookVersion.objects.create(refbook=cls.refbook, version='1.0', start_date=date(2022, 1, 1))
        cls.element1 = RefbookElement.objects.create(version=cls.version, code='1', value='Therapist')
        cls.element2 = RefbookElement.objects.create(version=cls.version, code='2', value='Orthopedist')

    def test_get_refbooks(self):
        """
        Тест для проверки получения списка справочников через API с параметром даты.
        """
        response = self.client.get(reverse('refbooks-list'), {'date': '2022-10-01'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['refbooks']), 1)
        self.assertEqual(response.json()['refbooks'][0]['code'], 'RB1')

    def test_get_elements(self):
        """
        Тест для проверки получения элементов конкретного справочника через API.
        """
        response = self.client.get(reverse('refbooks-elements', args=[self.refbook.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['elements']), 2)
        self.assertEqual(response.json()['elements'][0]['code'], '1')
        self.assertEqual(response.json()['elements'][1]['value'], 'Orthopedist')

    def test_check_element_valid(self):
        """
        Тест для проверки валидации элемента справочника (корректный элемент).
        """
        response = self.client.get(reverse('check-element', args=[self.refbook.id]), {'code': '1', 'value': 'Therapist'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['valid'])

    def test_check_element_invalid(self):
        """
        Тест для проверки валидации элемента справочника (некорректный элемент).
        """
        response = self.client.get(reverse('check-element', args=[self.refbook.id]), {'code': '1', 'value': 'Unknown'})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()['valid'])
