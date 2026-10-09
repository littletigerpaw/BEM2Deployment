from flask import jsonify, request
from marshmallow import ValidationError

from app.blueprints.inventory import inventory_bp
from app.blueprints.inventory.schemas import inventory_schema, inventories_schema
from app.extensions import cache, db
from app.models.inventory import Inventory


@inventory_bp.post("/")
def create_inventory_item():
    try:
        inventory_item = inventory_schema.load(request.get_json() or {})
    except ValidationError as err:
        return jsonify(err.messages), 400

    db.session.add(inventory_item)
    db.session.commit()
    return inventory_schema.jsonify(inventory_item), 201


@inventory_bp.get("/")
@cache.cached(timeout=60)
def get_inventory_items():
    inventory_items = Inventory.query.all()
    return inventories_schema.jsonify(inventory_items), 200


@inventory_bp.get("/<int:inventory_id>")
def get_inventory_item(inventory_id):
    inventory_item = Inventory.query.get_or_404(inventory_id)
    return inventory_schema.jsonify(inventory_item), 200


@inventory_bp.put("/<int:inventory_id>")
def update_inventory_item(inventory_id):
    inventory_item = Inventory.query.get_or_404(inventory_id)
    payload = request.get_json() or {}

    for field in ["name", "price"]:
        if field in payload:
            setattr(inventory_item, field, payload[field])

    db.session.commit()
    return inventory_schema.jsonify(inventory_item), 200


@inventory_bp.delete("/<int:inventory_id>")
def delete_inventory_item(inventory_id):
    inventory_item = Inventory.query.get_or_404(inventory_id)
    db.session.delete(inventory_item)
    db.session.commit()
    return jsonify({"message": f"Inventory item {inventory_id} deleted"}), 200
