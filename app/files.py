from pathlib import Path
from flask import Blueprint, abort, send_file
from .auth import require_auth

bp = Blueprint("files", __name__)
BASE_DIR = (Path(__file__).resolve().parent.parent / "uploads").resolve()


@bp.get("/files/<path:name>")
@require_auth
def download(name):
    target = (BASE_DIR / name).resolve()
    if BASE_DIR not in target.parents and target != BASE_DIR:
        abort(400, "invalid path")
    if not target.is_file():
        abort(404)
    return send_file(target)
