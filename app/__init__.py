from flask import Flask, jsonify
from flask_swagger_ui import get_swaggerui_blueprint

from app.extensions import cache, db, limiter, ma
from app.swagger_docs import build_swagger_spec
from config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    swagger_ui = get_swaggerui_blueprint(
        "/api/docs",
        "/swagger.json",
        config={"app_name": "Mechanic Shop API"},
    )
    app.register_blueprint(swagger_ui, url_prefix="/api/docs")

    db.init_app(app)
    ma.init_app(app)
    cache.init_app(app)
    limiter.init_app(app)

    from app.models import customer  # noqa: F401
    from app.models import inventory  # noqa: F401
    from app.models import mechanic  # noqa: F401
    from app.models import service_ticket  # noqa: F401

    from app.blueprints.customers import customers_bp
    from app.blueprints.inventory import inventory_bp
    from app.blueprints.mechanics import mechanics_bp
    from app.blueprints.service_tickets import service_tickets_bp

    app.register_blueprint(customers_bp, url_prefix="/customers")
    app.register_blueprint(mechanics_bp, url_prefix="/mechanics")
    app.register_blueprint(service_tickets_bp, url_prefix="/service-tickets")
    app.register_blueprint(inventory_bp, url_prefix="/inventory")

    with app.app_context():
        db.create_all()

    @app.get("/swagger.json")
    def swagger_json():
        return jsonify(build_swagger_spec(app)), 200

    @app.get("/")
    def health_check():
        return {"message": "Mechanic Shop API is running"}, 200

    return app
