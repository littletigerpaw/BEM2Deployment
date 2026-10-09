from marshmallow import Schema, ValidationError, fields

from app.extensions import ma
from app.models.customer import Customer


class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
        load_instance = True
        ordered = True

    password = fields.String(load_only=True, required=False, allow_none=True)
    service_ticket_ids = fields.Method("get_service_ticket_ids", dump_only=True)

    def get_service_ticket_ids(self, obj):
        return [ticket.id for ticket in obj.service_tickets]


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True)


customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)
login_schema = LoginSchema()
