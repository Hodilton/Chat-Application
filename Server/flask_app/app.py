from flask import Flask
from .routes.users import users_bp, init_users_routes
from .routes.chats import chats_bp, init_chats_routes

app = Flask(__name__)
db_global = None

def init_db(db):
    global db_global
    db_global = db

    init_users_routes(db)
    init_chats_routes(db)

    app.register_blueprint(users_bp)
    app.register_blueprint(chats_bp)
