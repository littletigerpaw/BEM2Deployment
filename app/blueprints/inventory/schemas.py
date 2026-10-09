from marshmallow import fields

from app.extensions import ma
from app.models.inventory import Inventory


class InventorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Inventory
        load_instance = True
        ordered = True

    ticket_ids = fields.Method("get_ticket_ids", dump_only=True)

    def get_ticket_ids(self, obj):
        return [ticket.id for ticket in obj.service_tickets]


inventory_schema = InventorySchema()
inventories_schema = InventorySchema(many=True)
