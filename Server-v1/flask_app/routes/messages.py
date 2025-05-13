from flask import Blueprint, request, jsonify
from datetime import datetime

messages_bp = Blueprint('messages', __name__)
db_global = None


def init_messages_routes(db):
    global db_global
    db_global = db


@messages_bp.route('/messages', methods=['POST'])
def send_message():
    try:
        data = request.get_json()
        required = ['chat_id', 'sender_id', 'content']
        if not all(key in data for key in required):
            return jsonify({"error": "Missing required fields"}), 400

        chat_id = int(data['chat_id'])
        sender_id = int(data['sender_id'])
        content = str(data['content']).strip()

        if not content:
            return jsonify({"error": "Message content cannot be empty"}), 400

        chat = db_global.tables.chats.fetch("by_id", "one", (chat_id,))
        if not chat:
            return jsonify({"error": "Chat not found"}), 404

        sender = db_global.tables.users.fetch("by_id", "one", (sender_id,))
        if not sender:
            return jsonify({"error": "Sender not found"}), 404

        message_data = (chat_id, sender_id, content)
        result_id = db_global.tables.messages.insert(message_data)

        message = db_global.tables.messages.fetch("by_id", "one", (result_id,))

        return jsonify({
            "id": message[0],
            "chat_id": chat_id,
            "content": content,
            "sent_at": message[4].strftime("%Y-%m-%d %H:%M:%S"),
            "sender": {
                "id": sender[0],
                "username": sender[1],
                "email": sender[2]
            }
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@messages_bp.route('/messages/<int:chat_id>', methods=['GET'])
def get_chat_messages(chat_id):
    try:
        messages = db_global.tables.messages.fetch("by_chat", "all", (chat_id,))

        result = [{
            "id": m[0],
            "chat_id": chat_id,
            "content": m[1],
            "sent_at":  m[2].strftime("%Y-%m-%d %H:%M:%S"),
            "sender": {
                "id": m[3],
                "username": m[4]
            }
        } for m in messages]

        return jsonify({
            "chat_id": chat_id,
            "count": len(result),
            "messages": result
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@messages_bp.route('/messages/<int:chat_id>/new', methods=['GET'])
def get_new_messages(chat_id):
    try:
        last_id = request.args.get('last_id', default=0, type=int)
        chat = db_global.tables.chats.fetch("by_id", "one", (chat_id,))
        if not chat:
            return jsonify({"error": "Chat not found"}), 404

        new_messages = db_global.tables.messages.fetch("new_messages", "all", (chat_id, last_id))

        result = [{
            "id": m[0],
            "content": m[1],
            "sent_at": m[2].strftime("%Y-%m-%d %H:%M:%S"),
            "sender": {
                "id": m[3],
                "username": m[4]
            }
        } for m in new_messages]

        return jsonify({
            "chat_id": chat_id,
            "count": len(result),
            "messages": result
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@messages_bp.route('/messages/<int:message_id>', methods=['DELETE'])
def delete_message(message_id):
    try:
        db_global.tables.messages.delete("by_id", (message_id,))
        return jsonify({"message": "Message deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500