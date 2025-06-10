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
        chat_id = int(data.get('chat_id'))
        sender_id = int(data.get('sender_id'))
        content = str(data.get('content', '')).strip()

        if not all([chat_id, sender_id, content]):
            return jsonify({"error": "Missing required message fields"}), 400

        if not db_global.tables.chats.fetch("by_id", "one", (chat_id,)):
            return jsonify({"error": "Chat not found"}), 404

        if not db_global.tables.users.fetch("by_id", "one", (sender_id,)):
            return jsonify({"error": "Sender not found"}), 404

        message_id = db_global.tables.messages.insert((chat_id, sender_id, content))
        message = db_global.tables.messages.fetch("by_id", "one", (message_id,))
        sender = db_global.tables.users.fetch("by_id", "one", (sender_id,))

        return jsonify({
            "id": message[0],
            "chat_id": message[1],
            "content": message[3],
            "sent_at": message[4].strftime("%Y-%m-%d %H:%M:%S"),
            "sender": {
                "id": sender[0],
                "username": sender[1],
                "email": sender[2]
            }
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@messages_bp.route('/messages/<int:message_id>', methods=['DELETE'])
def delete_message(message_id):
    try:
        db_global.tables.messages.delete("by_id", (message_id,))
        return jsonify({
            "message": "Message deleted"
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@messages_bp.route('/messages/<int:chat_id>', methods=['GET'])
def get_chat_messages(chat_id):
    try:
        messages = db_global.tables.messages.fetch("by_chat", "all", (chat_id,))
        result = [{
            "id": message[0],
            "chat_id": chat_id,
            "content": message[1],
            "sent_at": message[2].strftime("%Y-%m-%d %H:%M:%S"),
            "sender": {
                "id": message[3],
                "username": message[4]
            }
        } for message in messages]

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
        new_messages = db_global.tables.messages.fetch("new_messages", "all", (chat_id, last_id))
        result = [{
            "id": message[0],
            "content": message[1],
            "sent_at": message[2].strftime("%Y-%m-%d %H:%M:%S"),
            "sender": {
                "id": message[3],
                "username": message[4]
            }
        } for message in new_messages]

        return jsonify({
            "chat_id": chat_id,
            "count": len(result),
            "messages": result
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500