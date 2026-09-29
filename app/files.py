from pathlib import Path
from flask import Blueprint, abort, send_file
from .auth import require_auth

bp = Blueprint("files", __name__)
BASE_DIR = (Path(__file__).resolve().parent.parent / "uploads").resolve()


@bp.get("/files/<path:name>")
@require_auth
def download(name):
    # DEMO VULNERABILITY: no check that the resolved path stays inside BASE_DIR.
    target = BASE_DIR / name
    if not target.is_file():
        abort(404)
    return send_file(target)
