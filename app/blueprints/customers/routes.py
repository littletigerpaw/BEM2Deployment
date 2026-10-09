from functools import wraps

from flask import current_app, jsonify, request
from jose import JWTError, jwt
from marshmallow import ValidationError

from app.blueprints.customers import customers_bp
from app.blueprints.customers.schemas import customer_schema, customers_schema, login_schema
from app.extensions import cache, db, limiter
from app.models.customer import Customer
from app.models.service_ticket import ServiceTicket


def encode_token(customer_id):
    payload = {"customer_id": customer_id}
    return jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")


def decode_token(token):
    try:
        return jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
    except JWTError:
        return None


def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Bearer token is required"}), 401

        token = auth_header.split(" ", 1)[1].strip()
        payload = decode_token(token)
        if not payload or "customer_id" not in payload:
            return jsonify({"error": "Invalid or expired token"}), 401

        customer_id = payload["customer_id"]
        if args:
            args = (customer_id,) + args[1:]
        else:
            kwargs["customer_id"] = customer_id
        return func(*args, **kwargs)

    return wrapper


@customers_bp.post("/")
def create_customer():
    payload = request.get_json() or {}
    payload.setdefault("password", "")

    try:
        customer = customer_schema.load(payload)
    except ValidationError as err:
        return jsonify(err.messages), 400

    db.session.add(customer)
    db.session.commit()
    return customer_schema.jsonify(customer), 201


@customers_bp.post("/login")
def login_customer():
    try:
        data = login_schema.load(request.get_json() or {})
    except ValidationError as err:
        return jsonify(err.messages), 400

    customer = Customer.query.filter_by(email=data["email"]).first()
    if customer is None or customer.password != data["password"]:
        return jsonify({"error": "Invalid email or password"}), 401

    token = encode_token(customer.id)
    return jsonify({"token": token, "customer_id": customer.id}), 200


@customers_bp.get("/")
@limiter.limit("5/minute")
@cache.cached(timeout=60)
def get_customers():
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=10, type=int)
    pagination = Customer.query.paginate(page=page, per_page=per_page, error_out=False)
    payload = {
        "customers": customers_schema.dump(pagination.items),
        "page": pagination.page,
        "per_page": pagination.per_page,
        "total": pagination.total,
        "pages": pagination.pages,
    }
    return jsonify(payload), 200


@customers_bp.get("/<int:customer_id>")
def get_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    return customer_schema.jsonify(customer), 200


@customers_bp.get("/my-tickets")
@token_required
def get_customer_tickets(customer_id):
    tickets = ServiceTicket.query.filter_by(customer_id=customer_id).all()
    return jsonify([
        {
            "id": ticket.id,
            "customer_id": ticket.customer_id,
            "vin": ticket.vin,
            "issue_description": ticket.issue_description,
            "service_date": ticket.service_date.isoformat() if ticket.service_date else None,
            "status": ticket.status,
        }
        for ticket in tickets
    ]), 200


@customers_bp.put("/<int:customer_id>")
@token_required
def update_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    payload = request.get_json() or {}

    for field in ["name", "email", "phone", "password"]:
        if field in payload:
            setattr(customer, field, payload[field])

    db.session.commit()
    return customer_schema.jsonify(customer), 200


@customers_bp.delete("/<int:customer_id>")
@token_required
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": f"Customer {customer_id} deleted"}), 200
