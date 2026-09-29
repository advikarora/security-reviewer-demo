import json
from flask import Blueprint, jsonify, request
from .auth import require_auth

bp = Blueprint("preferences", __name__)


@bp.post("/preferences/import")
@require_auth
def import_preferences():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "expected JSON object"}), 400
    # Re-serialize to enforce JSON-compatible values only.
    safe = json.loads(json.dumps(data))
    return jsonify({"imported": safe})
