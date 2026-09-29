import base64
import pickle
from flask import Blueprint, jsonify, request
from .auth import require_auth

bp = Blueprint("preferences", __name__)


@bp.post("/preferences/import")
@require_auth
def import_preferences():
    body = request.get_json(silent=True) or {}
    raw = base64.b64decode(body.get("data", ""))
    # DEMO VULNERABILITY: pickle can execute attacker-controlled code during deserialization.
    preferences = pickle.loads(raw)
    return jsonify({"imported": preferences})
