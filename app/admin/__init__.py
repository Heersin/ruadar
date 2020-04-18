from flask import Blueprint

admin = Blueprint('admin', __name__, url_prefix='/')

from . import views, forms
