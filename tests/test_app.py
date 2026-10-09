from tests.base import APITestCase


class TestApp(APITestCase):
    def test_health_check(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["message"], "Mechanic Shop API is running")

    def test_swagger_json_endpoint(self):
        response = self.client.get("/swagger.json")
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["swagger"], "2.0")
        self.assertIn("/customers/", data["paths"])

    def test_swagger_ui_route(self):
        response = self.client.get("/api/docs/")
        self.assertEqual(response.status_code, 200)
