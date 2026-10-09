from tests.base import APITestCase


class TestMechanics(APITestCase):
    def test_create_mechanic_success(self):
        response = self.create_mechanic()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()["name"], "Mike Tech")

    def test_create_mechanic_negative_missing_specialty(self):
        response = self.client.post("/mechanics/", json={"name": "No Specialty"})
        self.assertEqual(response.status_code, 400)

    def test_get_mechanics_success(self):
        self.create_mechanic()
        response = self.client.get("/mechanics/")

        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.get_json()), 1)

    def test_get_mechanics_leaderboard_success(self):
        self.create_mechanic()
        response = self.client.get("/mechanics/leaderboard")

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)

    def test_update_mechanic_success(self):
        create_resp = self.create_mechanic()
        mechanic_id = create_resp.get_json()["id"]

        response = self.client.put(f"/mechanics/{mechanic_id}", json={"specialty": "Electrical"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["specialty"], "Electrical")

    def test_update_mechanic_negative_not_found(self):
        response = self.client.put("/mechanics/999", json={"specialty": "Electrical"})
        self.assertEqual(response.status_code, 404)

    def test_delete_mechanic_success(self):
        create_resp = self.create_mechanic(name="Delete Me", specialty="Tires")
        mechanic_id = create_resp.get_json()["id"]

        response = self.client.delete(f"/mechanics/{mechanic_id}")

        self.assertEqual(response.status_code, 200)
        self.assertIn("deleted", response.get_json()["message"].lower())

    def test_delete_mechanic_negative_not_found(self):
        response = self.client.delete("/mechanics/999")
        self.assertEqual(response.status_code, 404)
