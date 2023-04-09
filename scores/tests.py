from rest_framework import status
from rest_framework.test import APIClient, APITestCase


class YourModelViewSetTests(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_created_response(self):
        data = {
            "input_value": 1,
        }
        response = self.client.post("/scores/api/get_score/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_no_data(self):
        response = self.client.post("/scores/api/get_score/", format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_wrong_parameter_name(self):
        data = {
            "input_values": 1,
        }
        response = self.client.post("/scores/api/get_score/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_string_number_input(self):
        data = {
            "input_value": "1",
        }
        response = self.client.post("/scores/api/get_score/", data, format="json")
        self.assertEqual(response.data["score"], 2)

    def test_formula_invalid_input(self):
        data = {
            "input_value": "a",
        }
        response = self.client.post("/scores/api/get_score/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_anonymous_user(self):
        data = {
            "input_value": 1,
        }
        response = self.client.post("/scores/api/get_score/", data, format="json")
        self.assertEqual(response.data["user"], None)

    def test_formula(self):
        # Zero handling
        data = {
            "input_value": 0,
        }
        response = self.client.post("/scores/api/get_score/", data, format="json")
        self.assertEqual(response.data["score"], 1)

        # One handling
        data = {
            "input_value": 1,
        }
        response = self.client.post("/scores/api/get_score/", data, format="json")
        self.assertEqual(response.data["score"], 2)

        # Negative one handling
        data = {
            "input_value": -1,
        }
        response = self.client.post("/scores/api/get_score/", data, format="json")
        self.assertEqual(response.data["score"], 0)

        # Large negative number handling
        data = {
            "input_value": -99999,
        }
        response = self.client.post("/scores/api/get_score/", data, format="json")
        self.assertEqual(response.data["score"], -99998)

        # Large positive number handling
        data = {
            "input_value": 99999,
        }
        response = self.client.post("/scores/api/get_score/", data, format="json")
        self.assertEqual(response.data["score"], 100000)