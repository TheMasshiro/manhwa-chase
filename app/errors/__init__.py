from flask import Blueprint

errors_bp = Blueprint("errors", __name__, template_folder="template/errors")

from app.errors import error_handlers  # noqa: E402, F401
