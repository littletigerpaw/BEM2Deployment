import unittest

from app import create_app
from app.extensions import db
from config import TestingConfig


class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.ctx = self.app.app_context()
        self.ctx.push()

        db.drop_all()
        db.create_all()

        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def create_customer(self, name="Test Customer", email="customer@example.com", phone="555-111-2222", password="secret123"):
        response = self.client.post(
            "/customers/",
            json={
                "name": name,
                "email": email,
                "phone": phone,
                "password": password,
            },
        )
        return response

    def login_customer(self, email="customer@example.com", password="secret123"):
        return self.client.post(
            "/customers/login",
            json={"email": email, "password": password},
        )

    def create_mechanic(self, name="Mike Tech", specialty="Brakes"):
        return self.client.post(
            "/mechanics/",
            json={"name": name, "specialty": specialty},
        )

    def create_inventory_item(self, name="Oil Filter", price=19.99):
        return self.client.post(
            "/inventory/",
            json={"name": name, "price": price},
        )

    def create_service_ticket(self, customer_id, vin="VIN123456789", issue="Needs alignment"):
        return self.client.post(
            "/service-tickets/",
            json={
                "customer_id": customer_id,
                "vin": vin,
                "issue_description": issue,
            },
        )

    @staticmethod
    def auth_header(token):
        return {"Authorization": f"Bearer {token}"}
