from flask import Blueprint, request, jsonify

chats_bp = Blueprint('chats', __name__)
db_global = None


def init_chats_routes(db):
    global db_global
    db_global = db

@chats_bp.route('/chats/start', methods=['POST'])
def start_chat():
    try:
        data = request.get_json()
        user1_id = int(data.get('user1_id'))
        user2_id = int(data.get('user2_id'))

        if not user1_id or not user2_id:
            return jsonify({"error": "Both user IDs are required"}), 400

        sorted_user1 = min(int(user1_id), int(user2_id))
        sorted_user2 = max(int(user1_id), int(user2_id))

        existing_chat = db_global.tables.chats.fetch("by_users", "one",
                                                     (sorted_user1, sorted_user2, sorted_user1, sorted_user2))
        if existing_chat:
            return jsonify({
                "message": "Chat already exists",
                "chat_id": existing_chat[0]
            }), 200

        chat_id = db_global.tables.chats.insert((sorted_user1, sorted_user2, sorted_user1, sorted_user2))
        return jsonify({
            "message": "Chat started",
            "chat_id": chat_id
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@chats_bp.route('/chats', methods=['DELETE'])
def delete_chat_by_users():
    try:
        user1_id = request.args.get('user1_id', type=int)
        user2_id = request.args.get('user2_id', type=int)

        if not user1_id or not user2_id:
            return jsonify({
                "error": "Both user IDs are query required"
            }), 400

        sorted_user1 = min(user1_id, user2_id)
        sorted_user2 = max(user1_id, user2_id)

        db_global.tables.chats.delete("by_users", (sorted_user1, sorted_user2, sorted_user1, sorted_user2))

        return jsonify({
            "message": "Chat deleted successfully"
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@chats_bp.route('/chats', methods=['GET'])
def get_user_chats():
    try:
        user_id = request.args.get('user_id', type=int)
        if not user_id:
            return jsonify({
                "error": "Missing user_id parameter"
            }), 400

        chats = db_global.tables.chats.fetch("by_user", "all", (user_id, user_id))

        if not chats:
            return jsonify({
                "user_id": user_id,
                "message": "No chats found",
                "count": 0,
                "chats": []
            }), 200

        result = []
        for chat in chats:
            other_user_id = chat[1] if user_id != chat[1] else chat[2]
            other_user = db_global.tables.users.fetch("by_id", "one", (other_user_id,))

            if other_user:
                result.append({
                    "chat_id": chat[0],
                    "user": {
                        "id": other_user[0],
                        "username": other_user[1],
                        "email": other_user[2]
                    },
                    "created_at": chat[3].isoformat() if chat[3] else None
                })

        return jsonify({
            "user_id": user_id,
            "message": "Chats retrieved successfully",
            "count": len(result),
            "chats": result
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500