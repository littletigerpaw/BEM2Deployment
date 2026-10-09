from tests.base import APITestCase


class TestCustomers(APITestCase):
    def test_create_customer_success(self):
        response = self.create_customer()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()["email"], "customer@example.com")

    def test_create_customer_negative_missing_required_field(self):
        response = self.client.post(
            "/customers/",
            json={
                "name": "Missing Phone",
                "email": "valid@example.com",
                "password": "secret123",
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_login_customer_success(self):
        self.create_customer()
        response = self.login_customer()
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.get_json())

    def test_login_customer_negative_bad_password(self):
        self.create_customer()
        response = self.login_customer(password="wrong-password")
        self.assertEqual(response.status_code, 401)

    def test_get_customers_success(self):
        self.create_customer()
        response = self.client.get("/customers/")
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(data["total"], 1)
        self.assertIn("customers", data)

    def test_get_customer_by_id_and_negative_not_found(self):
        create_resp = self.create_customer()
        customer_id = create_resp.get_json()["id"]

        found_resp = self.client.get(f"/customers/{customer_id}")
        not_found_resp = self.client.get("/customers/999")

        self.assertEqual(found_resp.status_code, 200)
        self.assertEqual(not_found_resp.status_code, 404)

    def test_get_my_tickets_success(self):
        create_resp = self.create_customer()
        customer_id = create_resp.get_json()["id"]
        login_resp = self.login_customer()
        token = login_resp.get_json()["token"]

        self.create_service_ticket(customer_id=customer_id, issue="Engine knock")
        response = self.client.get("/customers/my-tickets", headers=self.auth_header(token))

        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.get_json()), 1)

    def test_get_my_tickets_negative_missing_token(self):
        response = self.client.get("/customers/my-tickets")
        self.assertEqual(response.status_code, 401)

    def test_update_customer_success(self):
        create_resp = self.create_customer()
        customer_id = create_resp.get_json()["id"]
        token = self.login_customer().get_json()["token"]

        response = self.client.put(
            f"/customers/{customer_id}",
            json={"phone": "555-999-0000"},
            headers=self.auth_header(token),
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["phone"], "555-999-0000")

    def test_update_customer_negative_invalid_token(self):
        create_resp = self.create_customer()
        customer_id = create_resp.get_json()["id"]

        response = self.client.put(
            f"/customers/{customer_id}",
            json={"name": "Updated"},
            headers=self.auth_header("bad.token.value"),
        )

        self.assertEqual(response.status_code, 401)

    def test_delete_customer_success(self):
        create_resp = self.create_customer()
        customer_id = create_resp.get_json()["id"]
        token = self.login_customer().get_json()["token"]

        response = self.client.delete(
            f"/customers/{customer_id}",
            headers=self.auth_header(token),
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("deleted", response.get_json()["message"].lower())

    def test_delete_customer_negative_missing_token(self):
        create_resp = self.create_customer(email="delete2@example.com")
        customer_id = create_resp.get_json()["id"]

        response = self.client.delete(f"/customers/{customer_id}")
        self.assertEqual(response.status_code, 401)
