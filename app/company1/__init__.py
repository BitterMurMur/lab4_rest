from flask import Blueprint

bp = Blueprint('company1', __name__)

from app.company1 import app
