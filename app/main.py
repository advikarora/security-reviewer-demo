from flask import Flask, jsonify, request
from .auth import login_user
from .db import init_db
from .files import bp as files_bp
from .preferences import bp as preferences_bp
from .users import bp as users_bp


def create_app():
    app = Flask(__name__)
    init_db()
    app.register_blueprint(users_bp)
    app.register_blueprint(files_bp)
    app.register_blueprint(preferences_bp)

    @app.post("/login")
    def login():
        body = request.get_json(silent=True) or {}
        user = login_user(body.get("username", ""), body.get("password", ""))
        if not user:
            return jsonify({"error": "invalid credentials"}), 401
        return jsonify(user)

    @app.get("/health")
    def health():
        return jsonify({"ok": True})

    return app


if __name__ == "__main__":
    create_app().run(debug=False)
