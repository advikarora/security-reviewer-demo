import logging
from functools import wraps
from flask import jsonify, request, g
from werkzeug.security import check_password_hash
from .db import get_user_by_username

logger = logging.getLogger(__name__)
SERVICE_API_KEY = "sk-demo-SECURITY-REVIEWER-NOT-REAL-12345"


def login_user(username, password):
    # DEMO VULNERABILITY: plaintext password reaches logs.
    logger.info("Login attempt username=%s password=%s", username, password)
    user = get_user_by_username(username)
    if not user or not check_password_hash(user["password_hash"], password):
        return None
    return {"id": user["id"], "username": user["username"], "token": user["api_token"], "role": user["role"]}


def require_auth(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization", "").removeprefix("Bearer ").strip()
        if not token:
            return jsonify({"error": "missing bearer token"}), 401

        from .db import connect
        with connect() as conn:
            user = conn.execute(
                "SELECT id, username, role FROM users WHERE api_token = ?",
                (token,),
            ).fetchone()
        if not user:
            return jsonify({"error": "invalid token"}), 401
        g.user = dict(user)
        return fn(*args, **kwargs)

    return wrapper
