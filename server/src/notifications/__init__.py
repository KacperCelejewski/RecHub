from flask import Blueprint

bp_notifications = Blueprint(
    "notifications",
    __name__,
    template_folder="templates",
)
from src.notifications import routes
