from flask import Blueprint, request, jsonify

users_bp = Blueprint('users', __name__)
db_global = None

def init_users_routes(db):
    global db_global
    db_global = db

@users_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = str(data['username'])
        email = str(data['email'])
        password_hash = str(data('password'))

        if not all([username, email, password_hash]):
            return jsonify({"error": "Missing required user fields"}), 400

        if db_global.tables.users.fetch("by_username", "one", (username,)):
            return jsonify({"error": "Username already exists"}), 400

        if db_global.tables.users.fetch("by_email", "one", (email,)):
            return jsonify({"error": "Email already registered"}), 400

        user_id = db_global.tables.users.insert((username, email, password_hash))
        return jsonify({
            "message": "User created",
            "user_id": user_id
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@users_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = str(data['email'])
        password_hash = str(data('password'))

        if not all([email, password_hash]):
            return jsonify({"error": "Missing required user fields"}), 400

        user = db_global.tables.users.fetch("by_email", "one", (email,))

        if not user or password != user[3]:
            return jsonify({"error": "Invalid email or password"}), 401

        return jsonify({
            "id": user[0],
            "username": user[1],
            "email": user[2],
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@users_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = db_global.tables.users.fetch("by_id", "one", (user_id,))
        if not user:
            return jsonify({"error": "User not found"}), 404

        if user:
            return jsonify({
                "id": user[0],
                "username": user[1],
                "email": user[2],
            }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@users_bp.route('/users', methods=['GET'])
def get_all_users():
    try:
        users = db_global.tables.users.fetch("all", "all")
        return jsonify([
            {
                "id": user[0],
                "username": user[1],
                "email": user[2],
            } for user in users
        ]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@users_bp.route('/users/exclude/<int:exclude_id>', methods=['GET'])
def get_users_exclude(exclude_id):
    try:
        users = db_global.tables.users.fetch("all_except", "all", (exclude_id,))
        return jsonify([
            {
                "id": user[0],
                "username": user[1],
                "email": user[2],
            } for user in users
        ]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500