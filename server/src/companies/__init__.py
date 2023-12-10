from flask import Blueprint

bp_companies = Blueprint(
    "companies",
    __name__,
    template_folder="templates",
)
from src.companies import routes
