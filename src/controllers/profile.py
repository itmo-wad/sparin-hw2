from os import abort
from flask import Blueprint, redirect, render_template, request, session, url_for, abort
from database import mongo
from wtforms import ValidationError

profile_page = Blueprint("profile_page", __name__, template_folder='templates')

@profile_page.route('/')
def index():
    if 'username' not in session:
        abort(403)

    return render_template(f'pages/profile/index.html')