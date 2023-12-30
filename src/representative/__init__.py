from flask import Blueprint

bp_representatives = Blueprint(
    "representatives",
    __name__,
    template_folder="templates",
)
from src.representative import routes
