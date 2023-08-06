from datetime import datetime
from django.test import TestCase

from django.urls import reverse
from rest_framework.fields import DateTimeField

from .models import FaqInfo


class RegistrationApiTest(TestCase):
    def setUp(self):
        self.faq_data = [
            {
                'title': 'test question 1',
                'answer': 'test answer 1',
                'number': 2,
                'created_at': datetime.now()
            },
            {
                'title': 'test question 2',
                'answer': 'test answer 2',
                'number': 3,
                'created_at': datetime.now()
            },
            {
                'title': 'test question third',
                'answer': 'test answer third',
                'number': 1,
                'created_at': datetime.now()
            }
        ]
        _test_faqs = [FaqInfo(**data) for data in self.faq_data]
        self.test_faqs = FaqInfo.objects.bulk_create(_test_faqs)

    def test_faq_get(self):
        response = self.client.get(
            reverse('garpix_faq:faq-list'),
            HTTP_ACCEPT='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [
            {
                'id': self.test_faqs[2].id,
                'title': self.faq_data[2]['title'],
                'answer': self.faq_data[2]['answer'],
                'number': self.faq_data[2]['number'],
                'created_at': DateTimeField().to_representation(self.test_faqs[2].created_at)
            },
            {
                'id': self.test_faqs[0].id,
                'title': self.faq_data[0]['title'],
                'answer': self.faq_data[0]['answer'],
                'number': self.faq_data[0]['number'],
                'created_at': DateTimeField().to_representation(self.test_faqs[0].created_at)
            },
            {
                'id': self.test_faqs[1].id,
                'title': self.faq_data[1]['title'],
                'answer': self.faq_data[1]['answer'],
                'number': self.faq_data[1]['number'],
                'created_at': DateTimeField().to_representation(self.test_faqs[1].created_at)
            },
        ])

    def test_faq_search(self):
        response = self.client.get(
            reverse('garpix_faq:faq-list') + '?search=third',
            HTTP_ACCEPT='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [
            {
                'id': self.test_faqs[2].id,
                'title': self.faq_data[2]['title'],
                'answer': self.faq_data[2]['answer'],
                'number': self.faq_data[2]['number'],
                'created_at': DateTimeField().to_representation(self.test_faqs[2].created_at)
            },
        ])
