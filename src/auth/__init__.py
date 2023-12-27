from flask import Blueprint

bp_auth = Blueprint(
    "auth",
    __name__,
    template_folder="templates",
)
from src.auth import routes
