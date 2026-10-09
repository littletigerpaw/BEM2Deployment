from flask import jsonify, request
from marshmallow import ValidationError

from app.blueprints.mechanics import mechanics_bp
from app.blueprints.mechanics.schemas import mechanic_schema, mechanics_schema
from app.extensions import cache, db
from app.models.mechanic import Mechanic


@mechanics_bp.post("/")
def create_mechanic():
    try:
        mechanic = mechanic_schema.load(request.get_json() or {})
    except ValidationError as err:
        return jsonify(err.messages), 400

    db.session.add(mechanic)
    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 201


@mechanics_bp.get("/")
@cache.cached(timeout=60)
def get_mechanics():
    mechanics = sorted(Mechanic.query.all(), key=lambda item: len(item.service_tickets), reverse=True)
    return mechanics_schema.jsonify(mechanics), 200


@mechanics_bp.get("/leaderboard")
def get_mechanics_leaderboard():
    mechanics = sorted(Mechanic.query.all(), key=lambda item: len(item.service_tickets), reverse=True)
    payload = [
        {
            "id": mechanic.id,
            "name": mechanic.name,
            "specialty": mechanic.specialty,
            "ticket_count": len(mechanic.service_tickets),
        }
        for mechanic in mechanics
    ]
    return jsonify(payload), 200


@mechanics_bp.put("/<int:id>")
def update_mechanic(id):
    mechanic = Mechanic.query.get_or_404(id)
    payload = request.get_json() or {}

    for field in ["name", "specialty"]:
        if field in payload:
            setattr(mechanic, field, payload[field])

    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 200


@mechanics_bp.delete("/<int:id>")
def delete_mechanic(id):
    mechanic = Mechanic.query.get_or_404(id)
    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({"message": f"Mechanic {id} deleted"}), 200
