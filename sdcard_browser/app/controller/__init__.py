from flask import Blueprint
blueprint = Blueprint('view',__name__)
from . import routes, events#,sdcard_metadata_22a