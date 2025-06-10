from flask import Blueprint, request, jsonify

chats_bp = Blueprint('chats', __name__)
db_global = None

def init_chats_routes(db):
    global db_global
    db_global = db

@chats_bp.route('/chats', methods=['POST'])
def create_chat():
    try:
        data = request.get_json()
        name = data.get('name')
        user_ids = data.get('user_ids', [])

        if not name or not isinstance(user_ids, list) or len(user_ids) < 2:
            return jsonify({"error": "Chat name and at least 2 user IDs are required"}), 400

        chat_id = db_global.tables.chats.insert((name,))
        for user_id in user_ids:
            db_global.tables.chat_members.insert((chat_id, user_id))

        return jsonify({
            "message": "Chat created",
            "chat_id": chat_id
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@chats_bp.route('/chats/<int:chat_id>', methods=['DELETE'])
def delete_chat(chat_id):
    try:
        db_global.tables.chats.delete("by_id", (chat_id,))
        return jsonify({
            "message": "Chat deleted"
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@chats_bp.route('/chats', methods=['GET'])
def get_user_chats():
    try:
        user_id = request.args.get('user_id', type=int)
        if not user_id:
            return jsonify({"error": "Missing required user fields"}), 400

        chat_ids = db_global.tables.chat_members.fetch("chats_by_user", "all", (user_id,))

        chats = []
        for row in chat_ids:
            # other_user_id = chat[1] if user_id != chat[1] else chat[2]
            chat = db_global.tables.chats.fetch("by_id", "one", (row[0],))
            if not chat:
                continue
            members = db_global.tables.chat_members.fetch("members_by_chat", "all", (row[0],))
            chats.append({
                "chat_id": chat[0],
                "name": chat[1],
                "created_at": chat[2].isoformat() if chat[2] else None,
                "members": [{"id": m[0], "username": m[1], "email": m[2]} for m in members]
            })

        return jsonify({
            "user_id": user_id,
            "chats": chats
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500