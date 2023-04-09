from rest_framework import status
from rest_framework.test import APIClient, APITestCase

class YourModelViewSetTests(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_view_functionality(self):
        # Test the view functionality
        data = {'input_value': 9,}
        response = self.client.post('/scores/api/get_score/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['score'], 10)
        self.assertEqual(response.data['user'], None)