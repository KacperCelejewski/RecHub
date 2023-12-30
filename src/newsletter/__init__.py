from flask import Blueprint

bp_newsletter = Blueprint(
    "newesletter",
    __name__,
    template_folder="templates",
)
from src.newsletter import routes
