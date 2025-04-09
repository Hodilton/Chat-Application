from flask import Blueprint, request, jsonify

users_bp = Blueprint('users', __name__)
db_global = None

def init_users_routes(db):
    global db_global
    db_global = db


@users_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        required = ['email', 'password']
        if not all(key in data for key in required):
            return jsonify({"error": "Missing email or password."}), 400

        email = data['email']
        password = data['password']

        user = db_global.tables.users.fetch("by_email", "one", (email,))

        if not user:
            return jsonify({"error": "Invalid email."}), 401

        if password != user[3]:
            return jsonify({"error": "Invalid password"}), 401

        return jsonify({
            "id": user[0],
            "username": user[1],
            "email": user[2],
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@users_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        required = ['username', 'email', 'password']
        if not all(key in data for key in required):
            return jsonify({"error": "Missing required fields"}), 400

        existing_user = db_global.tables.users.fetch("by_username", "one", (data['username'],))
        if existing_user:
            return jsonify({"error": "Username already exists"}), 400

        existing_email = db_global.tables.users.fetch("by_email", "one", (data['email'],))
        if existing_email:
            return jsonify({"error": "Email already registered"}), 400

        user_data = (
            data['username'],
            data['email'],
            data['password']
        )

        user_id = db_global.tables.users.insert(user_data)
        return jsonify({"message": "User created", "user_id": user_id}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@users_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = db_global.tables.users.fetch("by_id", "one", (user_id,))
        if user:
            return jsonify({
                "id": user[0],
                "username": user[1],
                "email": user[2],
            }), 200
        return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@users_bp.route('/users', methods=['GET'])
def get_all_users():
    try:
        users = db_global.tables.users.fetch("all", "all")
        return jsonify([
            {
                "id": u[0],
                "username": u[1],
                "email": u[2],
            } for u in users
        ]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
