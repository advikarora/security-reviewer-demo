from flask import Blueprint, jsonify, g
from .auth import require_auth
from .db import get_user_by_id

bp = Blueprint("users", __name__)


@bp.get("/users/<int:user_id>")
@require_auth
def get_user(user_id):
    if g.user["id"] != user_id and g.user["role"] != "admin":
        return jsonify({"error": "forbidden"}), 403

    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "not found"}), 404
    return jsonify({"id": user["id"], "username": user["username"], "role": user["role"]})
