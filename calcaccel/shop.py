from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import session

from calcaccel.db import query, execute
from calcaccel.auth import login_required
from calcaccel.config import conf

import time
import json

bp = Blueprint("shop", __name__, url_prefix="/shop")
