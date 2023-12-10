from flask import Blueprint

bp_opinion = Blueprint(
    "opinion",
    __name__,
    template_folder="templates",
)
from src.opinions import routes
