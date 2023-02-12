from flask import Blueprint

bp = Blueprint('company2', __name__)

from app.company2 import app
