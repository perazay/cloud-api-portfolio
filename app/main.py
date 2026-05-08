import os
import time
import logging
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import URL

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

DB_USER = os.environ.get("DB_USER", "root")
DB_PASS = os.environ.get("DB_PASS", "")
DB_NAME = os.environ.get("DB_NAME", "portfolio-api")
INSTANCE_CONNECTION_NAME = os.environ.get("INSTANCE_CONNECTION_NAME")

app.config["SQLALCHEMY_DATABASE_URI"] = URL.create(
    drivername="mysql+pymysql",
    username=DB_USER,
    password=DB_PASS,
    database=DB_NAME,
    query={
        "unix_socket": f"/cloudsql/{INSTANCE_CONNECTION_NAME}"
    }
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Item(db.Model):
    __tablename__ = "item"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(255))

@app.route("/")
def home():
    return jsonify({"message": "Cloud API is running", "service": "user-cloud-api"})

@app.route("/health")
def health():
    try:
        db.session.execute(db.text("SELECT 1"))
        return jsonify({"status": "healthy", "database": "connected"})
    except Exception as e:
        logging.error(f"Database health check failed: {e}")
        return jsonify({"status": "unhealthy", "database": "disconnected"}), 500

@app.route("/items", methods=["GET"])
def get_items():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    pagination = Item.query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        "items": [
            {"id": item.id, "name": item.name, "description": item.description}
            for item in pagination.items
        ],
        "page": page,
        "per_page": per_page,
        "total": pagination.total
    })

@app.route("/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = Item.query.get_or_404(item_id)
    return jsonify({"id": item.id, "name": item.name, "description": item.description})

@app.route("/items", methods=["POST"])
def create_item():
    data = request.get_json()

    if not data or not data.get("name"):
        logging.warning("Invalid POST request: missing name")
        return jsonify({"error": "name is required"}), 400

    item = Item(name=data["name"], description=data.get("description", ""))
    db.session.add(item)
    db.session.commit()

    logging.info(f"Created item {item.id}")
    return jsonify({"id": item.id, "name": item.name, "description": item.description}), 201

@app.route("/items/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    item = Item.query.get_or_404(item_id)
    data = request.get_json() or {}

    item.name = data.get("name", item.name)
    item.description = data.get("description", item.description)

    db.session.commit()
    return jsonify({"id": item.id, "name": item.name, "description": item.description})

@app.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)

    db.session.delete(item)
    db.session.commit()

    return jsonify({"message": "Item deleted"})

@app.route("/simulate-failure")
def simulate_failure():
    logging.error("Simulated failure triggered")
    return jsonify({"error": "Simulated failure"}), 500

@app.route("/slow")
def slow_response():
    time.sleep(3)
    return jsonify({"message": "Delayed response completed", "delay_seconds": 3})