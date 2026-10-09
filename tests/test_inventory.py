from tests.base import APITestCase


class TestInventory(APITestCase):
    def test_create_inventory_item_success(self):
        response = self.create_inventory_item()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()["name"], "Oil Filter")

    def test_create_inventory_item_negative_missing_price(self):
        response = self.client.post("/inventory/", json={"name": "No Price"})
        self.assertEqual(response.status_code, 400)

    def test_get_inventory_items_success(self):
        self.create_inventory_item()
        response = self.client.get("/inventory/")

        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.get_json()), 1)

    def test_get_inventory_item_by_id_and_negative_not_found(self):
        create_resp = self.create_inventory_item()
        inventory_id = create_resp.get_json()["id"]

        found_resp = self.client.get(f"/inventory/{inventory_id}")
        not_found_resp = self.client.get("/inventory/999")

        self.assertEqual(found_resp.status_code, 200)
        self.assertEqual(not_found_resp.status_code, 404)

    def test_update_inventory_item_success(self):
        create_resp = self.create_inventory_item()
        inventory_id = create_resp.get_json()["id"]

        response = self.client.put(f"/inventory/{inventory_id}", json={"price": 25.5})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["price"], 25.5)

    def test_update_inventory_item_negative_not_found(self):
        response = self.client.put("/inventory/999", json={"price": 18.0})
        self.assertEqual(response.status_code, 404)

    def test_delete_inventory_item_success(self):
        create_resp = self.create_inventory_item(name="Delete Part", price=10.0)
        inventory_id = create_resp.get_json()["id"]

        response = self.client.delete(f"/inventory/{inventory_id}")

        self.assertEqual(response.status_code, 200)
        self.assertIn("deleted", response.get_json()["message"].lower())

    def test_delete_inventory_item_negative_not_found(self):
        response = self.client.delete("/inventory/999")
        self.assertEqual(response.status_code, 404)
