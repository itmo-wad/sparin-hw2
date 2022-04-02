from os import stat
from flask_pymongo import DESCENDING, PyMongo
import markdown
from datetime import datetime
from unicodedata import category
import uuid
from flask import Blueprint, abort, jsonify, redirect, render_template, request, session, url_for
from database import mongo
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import ValidationError
from bson.objectid import ObjectId

from forms.posts.CreatePostFrom import CreatePostForm

cards_page = Blueprint("cards_page", __name__, template_folder='templates')
POSTS_THEMES_FOLDER = './src/static/posts/'

cards = [
    { "id": 1, "en": "Card", "ru": "RU_Карточка"},
    { "id": 2, "en": "Category", "ru": "RU_Категория"},
    { "id": 3, "en": "Phone", "ru": "RU_Телефон"},
]

card_stats = {
    "1": False,
    "2": False,
    "3": False,
}

@cards_page.route('game')
def game():

    return render_template('pages/cards/index.html')

@cards_page.route('')
def getAll():
    return jsonify(cards)

@cards_page.route('/<id_card>', methods=["POST"])
def update_status(id_card):
    is_known = request.args.get("isKnown", None)
    if is_known is None:
        abort(400)

    card_stats[id_card] = False if is_known == 'false' else True
    return ('', 204)

@cards_page.route('stats')
def stats():

    return jsonify(card_stats)
