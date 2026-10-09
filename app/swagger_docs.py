from flask_swagger import swagger


def build_swagger_spec(app):
    generated = swagger(app)

    spec = {
        "swagger": "2.0",
        "info": {
            "title": "Mechanic Shop API",
            "description": "API documentation for customers, mechanics, service tickets, and inventory endpoints.",
            "version": "1.0.0",
        },
        "host": app.config.get("SWAGGER_HOST", generated.get("host", "127.0.0.1:5000")),
        "basePath": "/",
        "schemes": app.config.get("SWAGGER_SCHEMES", ["http"]),
        "tags": [
            {"name": "Health", "description": "Application health checks"},
            {"name": "Customers", "description": "Customer account and profile operations"},
            {"name": "Mechanics", "description": "Mechanic management operations"},
            {"name": "Service Tickets", "description": "Service ticket workflow operations"},
            {"name": "Inventory", "description": "Inventory management operations"},
        ],
        "securityDefinitions": {
            "BearerAuth": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "Use Bearer <token>",
            }
        },
        "definitions": {
            "CustomerPayload": {
                "type": "object",
                "required": ["name", "email", "phone", "password"],
                "properties": {
                    "name": {"type": "string", "example": "Jane Doe"},
                    "email": {"type": "string", "format": "email", "example": "jane@example.com"},
                    "phone": {"type": "string", "example": "555-222-3333"},
                    "password": {"type": "string", "example": "secret123"},
                },
            },
            "CustomerUpdatePayload": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "example": "Jane D."},
                    "email": {"type": "string", "format": "email", "example": "jane.new@example.com"},
                    "phone": {"type": "string", "example": "555-111-9999"},
                    "password": {"type": "string", "example": "newpassword123"},
                },
            },
            "LoginPayload": {
                "type": "object",
                "required": ["email", "password"],
                "properties": {
                    "email": {"type": "string", "format": "email", "example": "jane@example.com"},
                    "password": {"type": "string", "example": "secret123"},
                },
            },
            "CustomerResponse": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer", "example": 1},
                    "name": {"type": "string", "example": "Jane Doe"},
                    "email": {"type": "string", "example": "jane@example.com"},
                    "phone": {"type": "string", "example": "555-222-3333"},
                    "service_ticket_ids": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "example": [1, 2],
                    },
                },
            },
            "CustomerListResponse": {
                "type": "object",
                "properties": {
                    "customers": {
                        "type": "array",
                        "items": {"$ref": "#/definitions/CustomerResponse"},
                    },
                    "page": {"type": "integer", "example": 1},
                    "per_page": {"type": "integer", "example": 10},
                    "total": {"type": "integer", "example": 25},
                    "pages": {"type": "integer", "example": 3},
                },
            },
            "LoginResponse": {
                "type": "object",
                "properties": {
                    "token": {"type": "string", "example": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."},
                    "customer_id": {"type": "integer", "example": 1},
                },
            },
            "MechanicPayload": {
                "type": "object",
                "required": ["name", "specialty"],
                "properties": {
                    "name": {"type": "string", "example": "Alex Ramirez"},
                    "specialty": {"type": "string", "example": "Transmission"},
                },
            },
            "MechanicResponse": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer", "example": 1},
                    "name": {"type": "string", "example": "Alex Ramirez"},
                    "specialty": {"type": "string", "example": "Transmission"},
                    "ticket_ids": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "example": [1],
                    },
                },
            },
            "MechanicLeaderboardResponse": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer", "example": 1},
                        "name": {"type": "string", "example": "Alex Ramirez"},
                        "specialty": {"type": "string", "example": "Transmission"},
                        "ticket_count": {"type": "integer", "example": 3},
                    },
                },
            },
            "InventoryPayload": {
                "type": "object",
                "required": ["name", "price"],
                "properties": {
                    "name": {"type": "string", "example": "Brake Pad Set"},
                    "price": {"type": "number", "format": "float", "example": 79.99},
                },
            },
            "InventoryResponse": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer", "example": 1},
                    "name": {"type": "string", "example": "Brake Pad Set"},
                    "price": {"type": "number", "format": "float", "example": 79.99},
                    "ticket_ids": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "example": [1],
                    },
                },
            },
            "ServiceTicketPayload": {
                "type": "object",
                "required": ["customer_id", "vin", "issue_description"],
                "properties": {
                    "customer_id": {"type": "integer", "example": 1},
                    "vin": {"type": "string", "example": "1HGCM82633A004352"},
                    "issue_description": {"type": "string", "example": "Brake pedal feels soft"},
                    "status": {"type": "string", "example": "open"},
                },
            },
            "TicketEditPayload": {
                "type": "object",
                "properties": {
                    "add_ids": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "example": [1, 2],
                    },
                    "remove_ids": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "example": [3],
                    },
                },
            },
            "TicketPartPayload": {
                "type": "object",
                "required": ["inventory_id"],
                "properties": {
                    "inventory_id": {"type": "integer", "example": 1},
                },
            },
            "ServiceTicketResponse": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer", "example": 1},
                    "customer_id": {"type": "integer", "example": 1},
                    "vin": {"type": "string", "example": "1HGCM82633A004352"},
                    "issue_description": {"type": "string", "example": "Brake pedal feels soft"},
                    "service_date": {"type": "string", "example": "2026-10-09"},
                    "status": {"type": "string", "example": "open"},
                },
            },
            "ErrorResponse": {
                "type": "object",
                "properties": {
                    "error": {"type": "string", "example": "Invalid or expired token"}
                },
            },
            "MessageResponse": {
                "type": "object",
                "properties": {
                    "message": {"type": "string", "example": "Customer 1 deleted"}
                },
            },
        },
        "paths": {
            "/": {
                "get": {
                    "tags": ["Health"],
                    "summary": "API health check",
                    "description": "Confirms that the API service is running.",
                    "responses": {
                        "200": {
                            "description": "Service is healthy",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "message": {"type": "string", "example": "Mechanic Shop API is running"}
                                },
                            },
                        }
                    },
                }
            },
            "/customers/": {
                "post": {
                    "tags": ["Customers"],
                    "summary": "Create customer",
                    "description": "Creates a new customer account.",
                    "parameters": [
                        {
                            "in": "body",
                            "name": "payload",
                            "required": True,
                            "schema": {"$ref": "#/definitions/CustomerPayload"},
                        }
                    ],
                    "responses": {
                        "201": {
                            "description": "Customer created",
                            "schema": {"$ref": "#/definitions/CustomerResponse"},
                        },
                        "400": {
                            "description": "Validation error",
                            "schema": {"$ref": "#/definitions/ErrorResponse"},
                        },
                    },
                },
                "get": {
                    "tags": ["Customers"],
                    "summary": "List customers",
                    "description": "Returns a paginated list of customers.",
                    "responses": {
                        "200": {
                            "description": "Customer list",
                            "schema": {"$ref": "#/definitions/CustomerListResponse"},
                        }
                    },
                },
            },
            "/customers/login": {
                "post": {
                    "tags": ["Customers"],
                    "summary": "Customer login",
                    "description": "Authenticates a customer and returns a bearer token.",
                    "parameters": [
                        {
                            "in": "body",
                            "name": "payload",
                            "required": True,
                            "schema": {"$ref": "#/definitions/LoginPayload"},
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Login success",
                            "schema": {"$ref": "#/definitions/LoginResponse"},
                        },
                        "401": {
                            "description": "Invalid credentials",
                            "schema": {"$ref": "#/definitions/ErrorResponse"},
                        },
                    },
                }
            },
            "/customers/{customer_id}": {
                "get": {
                    "tags": ["Customers"],
                    "summary": "Get customer by ID",
                    "description": "Returns one customer by ID.",
                    "parameters": [
                        {
                            "name": "customer_id",
                            "in": "path",
                            "required": True,
                            "type": "integer",
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Customer found",
                            "schema": {"$ref": "#/definitions/CustomerResponse"},
                        },
                        "404": {"description": "Customer not found"},
                    },
                },
                "put": {
                    "tags": ["Customers"],
                    "summary": "Update customer",
                    "description": "Updates customer fields for the authenticated customer.",
                    "security": [{"BearerAuth": []}],
                    "parameters": [
                        {
                            "name": "customer_id",
                            "in": "path",
                            "required": True,
                            "type": "integer",
                        },
                        {
                            "in": "body",
                            "name": "payload",
                            "required": True,
                            "schema": {"$ref": "#/definitions/CustomerUpdatePayload"},
                        },
                    ],
                    "responses": {
                        "200": {
                            "description": "Customer updated",
                            "schema": {"$ref": "#/definitions/CustomerResponse"},
                        },
                        "401": {
                            "description": "Unauthorized",
                            "schema": {"$ref": "#/definitions/ErrorResponse"},
                        },
                    },
                },
                "delete": {
                    "tags": ["Customers"],
                    "summary": "Delete customer",
                    "description": "Deletes a customer account for the authenticated customer.",
                    "security": [{"BearerAuth": []}],
                    "parameters": [
                        {
                            "name": "customer_id",
                            "in": "path",
                            "required": True,
                            "type": "integer",
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Customer deleted",
                            "schema": {"$ref": "#/definitions/MessageResponse"},
                        },
                        "401": {
                            "description": "Unauthorized",
                            "schema": {"$ref": "#/definitions/ErrorResponse"},
                        },
                    },
                },
            },
            "/customers/my-tickets": {
                "get": {
                    "tags": ["Customers"],
                    "summary": "Get authenticated customer tickets",
                    "description": "Returns tickets associated with the authenticated customer.",
                    "security": [{"BearerAuth": []}],
                    "responses": {
                        "200": {
                            "description": "List of tickets",
                            "schema": {
                                "type": "array",
                                "items": {"$ref": "#/definitions/ServiceTicketResponse"},
                            },
                        },
                        "401": {
                            "description": "Unauthorized",
                            "schema": {"$ref": "#/definitions/ErrorResponse"},
                        },
                    },
                }
            },
            "/mechanics/": {
                "post": {
                    "tags": ["Mechanics"],
                    "summary": "Create mechanic",
                    "description": "Creates a mechanic record.",
                    "parameters": [
                        {
                            "in": "body",
                            "name": "payload",
                            "required": True,
                            "schema": {"$ref": "#/definitions/MechanicPayload"},
                        }
                    ],
                    "responses": {
                        "201": {
                            "description": "Mechanic created",
                            "schema": {"$ref": "#/definitions/MechanicResponse"},
                        },
                        "400": {
                            "description": "Validation error",
                            "schema": {"$ref": "#/definitions/ErrorResponse"},
                        },
                    },
                },
                "get": {
                    "tags": ["Mechanics"],
                    "summary": "List mechanics",
                    "description": "Returns all mechanics sorted by assigned ticket count.",
                    "responses": {
                        "200": {
                            "description": "Mechanic list",
                            "schema": {
                                "type": "array",
                                "items": {"$ref": "#/definitions/MechanicResponse"},
                            },
                        }
                    },
                },
            },
            "/mechanics/leaderboard": {
                "get": {
                    "tags": ["Mechanics"],
                    "summary": "Mechanic leaderboard",
                    "description": "Returns mechanics with ticket counts for ranking.",
                    "responses": {
                        "200": {
                            "description": "Leaderboard data",
                            "schema": {"$ref": "#/definitions/MechanicLeaderboardResponse"},
                        }
                    },
                }
            },
            "/mechanics/{id}": {
                "put": {
                    "tags": ["Mechanics"],
                    "summary": "Update mechanic",
                    "description": "Updates mechanic fields.",
                    "parameters": [
                        {"name": "id", "in": "path", "required": True, "type": "integer"},
                        {
                            "in": "body",
                            "name": "payload",
                            "required": True,
                            "schema": {"$ref": "#/definitions/MechanicPayload"},
                        },
                    ],
                    "responses": {
                        "200": {
                            "description": "Mechanic updated",
                            "schema": {"$ref": "#/definitions/MechanicResponse"},
                        },
                        "404": {"description": "Mechanic not found"},
                    },
                },
                "delete": {
                    "tags": ["Mechanics"],
                    "summary": "Delete mechanic",
                    "description": "Deletes a mechanic record.",
                    "parameters": [
                        {"name": "id", "in": "path", "required": True, "type": "integer"}
                    ],
                    "responses": {
                        "200": {
                            "description": "Mechanic deleted",
                            "schema": {"$ref": "#/definitions/MessageResponse"},
                        },
                        "404": {"description": "Mechanic not found"},
                    },
                },
            },
            "/inventory/": {
                "post": {
                    "tags": ["Inventory"],
                    "summary": "Create inventory item",
                    "description": "Creates an inventory part.",
                    "parameters": [
                        {
                            "in": "body",
                            "name": "payload",
                            "required": True,
                            "schema": {"$ref": "#/definitions/InventoryPayload"},
                        }
                    ],
                    "responses": {
                        "201": {
                            "description": "Inventory item created",
                            "schema": {"$ref": "#/definitions/InventoryResponse"},
                        },
                        "400": {
                            "description": "Validation error",
                            "schema": {"$ref": "#/definitions/ErrorResponse"},
                        },
                    },
                },
                "get": {
                    "tags": ["Inventory"],
                    "summary": "List inventory",
                    "description": "Returns all inventory items.",
                    "responses": {
                        "200": {
                            "description": "Inventory list",
                            "schema": {
                                "type": "array",
                                "items": {"$ref": "#/definitions/InventoryResponse"},
                            },
                        }
                    },
                },
            },
            "/inventory/{inventory_id}": {
                "get": {
                    "tags": ["Inventory"],
                    "summary": "Get inventory item",
                    "description": "Returns one inventory item by ID.",
                    "parameters": [
                        {
                            "name": "inventory_id",
                            "in": "path",
                            "required": True,
                            "type": "integer",
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Inventory item found",
                            "schema": {"$ref": "#/definitions/InventoryResponse"},
                        },
                        "404": {"description": "Inventory item not found"},
                    },
                },
                "put": {
                    "tags": ["Inventory"],
                    "summary": "Update inventory item",
                    "description": "Updates inventory item fields.",
                    "parameters": [
                        {
                            "name": "inventory_id",
                            "in": "path",
                            "required": True,
                            "type": "integer",
                        },
                        {
                            "in": "body",
                            "name": "payload",
                            "required": True,
                            "schema": {"$ref": "#/definitions/InventoryPayload"},
                        },
                    ],
                    "responses": {
                        "200": {
                            "description": "Inventory updated",
                            "schema": {"$ref": "#/definitions/InventoryResponse"},
                        },
                        "404": {"description": "Inventory item not found"},
                    },
                },
                "delete": {
                    "tags": ["Inventory"],
                    "summary": "Delete inventory item",
                    "description": "Deletes an inventory item.",
                    "parameters": [
                        {
                            "name": "inventory_id",
                            "in": "path",
                            "required": True,
                            "type": "integer",
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Inventory deleted",
                            "schema": {"$ref": "#/definitions/MessageResponse"},
                        },
                        "404": {"description": "Inventory item not found"},
                    },
                },
            },
            "/service-tickets/": {
                "post": {
                    "tags": ["Service Tickets"],
                    "summary": "Create service ticket",
                    "description": "Creates a new service ticket for an existing customer.",
                    "parameters": [
                        {
                            "in": "body",
                            "name": "payload",
                            "required": True,
                            "schema": {"$ref": "#/definitions/ServiceTicketPayload"},
                        }
                    ],
                    "responses": {
                        "201": {
                            "description": "Ticket created",
                            "schema": {"$ref": "#/definitions/ServiceTicketResponse"},
                        },
                        "400": {
                            "description": "Missing fields",
                            "schema": {"$ref": "#/definitions/ErrorResponse"},
                        },
                        "404": {
                            "description": "Customer not found",
                            "schema": {"$ref": "#/definitions/ErrorResponse"},
                        },
                    },
                },
                "get": {
                    "tags": ["Service Tickets"],
                    "summary": "List service tickets",
                    "description": "Returns all service tickets.",
                    "responses": {
                        "200": {
                            "description": "Ticket list",
                            "schema": {
                                "type": "array",
                                "items": {"$ref": "#/definitions/ServiceTicketResponse"},
                            },
                        }
                    },
                },
            },
            "/service-tickets/{ticket_id}/assign-mechanic/{mechanic_id}": {
                "put": {
                    "tags": ["Service Tickets"],
                    "summary": "Assign mechanic to ticket",
                    "description": "Assigns a mechanic to a service ticket.",
                    "parameters": [
                        {"name": "ticket_id", "in": "path", "required": True, "type": "integer"},
                        {"name": "mechanic_id", "in": "path", "required": True, "type": "integer"},
                    ],
                    "responses": {
                        "200": {
                            "description": "Mechanic assigned",
                            "schema": {"$ref": "#/definitions/ServiceTicketResponse"},
                        },
                        "404": {"description": "Ticket or mechanic not found"},
                    },
                }
            },
            "/service-tickets/{ticket_id}/remove-mechanic/{mechanic_id}": {
                "put": {
                    "tags": ["Service Tickets"],
                    "summary": "Remove mechanic from ticket",
                    "description": "Removes a mechanic from a service ticket.",
                    "parameters": [
                        {"name": "ticket_id", "in": "path", "required": True, "type": "integer"},
                        {"name": "mechanic_id", "in": "path", "required": True, "type": "integer"},
                    ],
                    "responses": {
                        "200": {
                            "description": "Mechanic removed",
                            "schema": {"$ref": "#/definitions/ServiceTicketResponse"},
                        },
                        "404": {"description": "Ticket or mechanic not found / not assigned"},
                    },
                }
            },
            "/service-tickets/{ticket_id}/edit": {
                "put": {
                    "tags": ["Service Tickets"],
                    "summary": "Bulk edit ticket mechanics",
                    "description": "Adds and removes mechanic assignments in one request.",
                    "parameters": [
                        {"name": "ticket_id", "in": "path", "required": True, "type": "integer"},
                        {
                            "in": "body",
                            "name": "payload",
                            "required": True,
                            "schema": {"$ref": "#/definitions/TicketEditPayload"},
                        },
                    ],
                    "responses": {
                        "200": {
                            "description": "Ticket updated",
                            "schema": {"$ref": "#/definitions/ServiceTicketResponse"},
                        },
                        "404": {"description": "Ticket not found"},
                    },
                }
            },
            "/service-tickets/{ticket_id}/parts": {
                "post": {
                    "tags": ["Service Tickets"],
                    "summary": "Add inventory part to ticket",
                    "description": "Associates an inventory part with a service ticket.",
                    "parameters": [
                        {"name": "ticket_id", "in": "path", "required": True, "type": "integer"},
                        {
                            "in": "body",
                            "name": "payload",
                            "required": True,
                            "schema": {"$ref": "#/definitions/TicketPartPayload"},
                        },
                    ],
                    "responses": {
                        "200": {
                            "description": "Part associated",
                            "schema": {"$ref": "#/definitions/ServiceTicketResponse"},
                        },
                        "400": {
                            "description": "Missing inventory_id",
                            "schema": {"$ref": "#/definitions/ErrorResponse"},
                        },
                        "404": {"description": "Ticket or inventory item not found"},
                    },
                }
            },
        },
    }

    return spec
