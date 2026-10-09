from tests.base import APITestCase


class TestServiceTickets(APITestCase):
    def _setup_customer_mechanic_inventory(self):
        customer_resp = self.create_customer()
        customer_id = customer_resp.get_json()["id"]

        mechanic_resp = self.create_mechanic()
        mechanic_id = mechanic_resp.get_json()["id"]

        inventory_resp = self.create_inventory_item()
        inventory_id = inventory_resp.get_json()["id"]

        return customer_id, mechanic_id, inventory_id

    def test_create_service_ticket_success(self):
        customer_id, _, _ = self._setup_customer_mechanic_inventory()
        response = self.create_service_ticket(customer_id=customer_id)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()["customer_id"], customer_id)

    def test_create_service_ticket_negative_missing_fields(self):
        response = self.client.post(
            "/service-tickets/",
            json={"customer_id": 1, "vin": "VIN123"},
        )
        self.assertEqual(response.status_code, 400)

    def test_get_service_tickets_success(self):
        customer_id, _, _ = self._setup_customer_mechanic_inventory()
        self.create_service_ticket(customer_id=customer_id)

        response = self.client.get("/service-tickets/")
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.get_json()), 1)

    def test_assign_mechanic_success(self):
        customer_id, mechanic_id, _ = self._setup_customer_mechanic_inventory()
        ticket_resp = self.create_service_ticket(customer_id=customer_id)
        ticket_id = ticket_resp.get_json()["id"]

        response = self.client.put(f"/service-tickets/{ticket_id}/assign-mechanic/{mechanic_id}")
        self.assertEqual(response.status_code, 200)

    def test_assign_mechanic_negative_not_found(self):
        response = self.client.put("/service-tickets/999/assign-mechanic/999")
        self.assertEqual(response.status_code, 404)

    def test_remove_mechanic_success(self):
        customer_id, mechanic_id, _ = self._setup_customer_mechanic_inventory()
        ticket_resp = self.create_service_ticket(customer_id=customer_id)
        ticket_id = ticket_resp.get_json()["id"]
        self.client.put(f"/service-tickets/{ticket_id}/assign-mechanic/{mechanic_id}")

        response = self.client.put(f"/service-tickets/{ticket_id}/remove-mechanic/{mechanic_id}")
        self.assertEqual(response.status_code, 200)

    def test_remove_mechanic_negative_not_assigned(self):
        customer_id, mechanic_id, _ = self._setup_customer_mechanic_inventory()
        ticket_resp = self.create_service_ticket(customer_id=customer_id)
        ticket_id = ticket_resp.get_json()["id"]

        response = self.client.put(f"/service-tickets/{ticket_id}/remove-mechanic/{mechanic_id}")
        self.assertEqual(response.status_code, 404)

    def test_edit_service_ticket_success(self):
        customer_id, mechanic_id, _ = self._setup_customer_mechanic_inventory()
        second_mechanic_resp = self.create_mechanic(name="Sam Wrench", specialty="Engine")
        second_mechanic_id = second_mechanic_resp.get_json()["id"]

        ticket_resp = self.create_service_ticket(customer_id=customer_id)
        ticket_id = ticket_resp.get_json()["id"]

        self.client.put(f"/service-tickets/{ticket_id}/assign-mechanic/{mechanic_id}")

        response = self.client.put(
            f"/service-tickets/{ticket_id}/edit",
            json={"add_ids": [second_mechanic_id], "remove_ids": [mechanic_id]},
        )
        self.assertEqual(response.status_code, 200)

    def test_edit_service_ticket_negative_not_found(self):
        response = self.client.put("/service-tickets/999/edit", json={"add_ids": [1], "remove_ids": []})
        self.assertEqual(response.status_code, 404)

    def test_add_inventory_part_to_ticket_success(self):
        customer_id, _, inventory_id = self._setup_customer_mechanic_inventory()
        ticket_resp = self.create_service_ticket(customer_id=customer_id)
        ticket_id = ticket_resp.get_json()["id"]

        response = self.client.post(
            f"/service-tickets/{ticket_id}/parts",
            json={"inventory_id": inventory_id},
        )

        self.assertEqual(response.status_code, 200)

    def test_add_inventory_part_to_ticket_negative_missing_inventory_id(self):
        customer_id, _, _ = self._setup_customer_mechanic_inventory()
        ticket_resp = self.create_service_ticket(customer_id=customer_id)
        ticket_id = ticket_resp.get_json()["id"]

        response = self.client.post(f"/service-tickets/{ticket_id}/parts", json={})
        self.assertEqual(response.status_code, 400)
