# app/routes/medicine_availability_routes.py

from flask import Blueprint, request, jsonify
from app.services import medicine_availablity_service as service

medicine_bp = Blueprint('medicine_bp', __name__)


# 🔹 Get all medicines
@medicine_bp.route('/medicines', methods=['GET'])
def get_all_medicines():
    try:
        medicines = service.get_all_medicines()
        return jsonify(medicines), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 🔹 Search medicine by name (for your Flutter search bar)
@medicine_bp.route('/medicines/search', methods=['GET'])
def search_medicine():
    name = request.args.get('name')
    if not name:
        return jsonify({"error": "Name query parameter is required"}), 400

    try:
        medicines = service.search_medicine_by_name(name)
        return jsonify(medicines), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 🔹 Get medicines by category (for category grid)
@medicine_bp.route('/medicines/category/<string:category>', methods=['GET'])
def get_by_category(category):
    try:
        medicines = service.get_medicines_by_category(category)
        return jsonify(medicines), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 🔹 Get low stock medicines
@medicine_bp.route('/medicines/low-stock', methods=['GET'])
def low_stock():
    try:
        medicines = service.get_low_stock_medicines()
        return jsonify(medicines), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 🔹 Get single medicine by ID
@medicine_bp.route('/medicines/<int:medicine_id>', methods=['GET'])
def get_medicine(medicine_id):
    medicine = service.get_medicine_by_id(medicine_id)
    if not medicine:
        return jsonify({"error": "Medicine not found"}), 404
    return jsonify(medicine), 200