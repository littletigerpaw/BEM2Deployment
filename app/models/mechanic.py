from app.extensions import db
from app.models.service_ticket import ticket_mechanics


class Mechanic(db.Model):
    __tablename__ = "mechanics"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    specialty = db.Column(db.String(120), nullable=False)

    service_tickets = db.relationship(
        "ServiceTicket",
        secondary=ticket_mechanics,
        back_populates="mechanics",
        lazy=True,
    )
