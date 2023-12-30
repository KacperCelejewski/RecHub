from flask import Blueprint

bp_main = Blueprint(
    "main",
    __name__,
    template_folder="templates",
)
from src.main import routes
