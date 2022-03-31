import os
from flask_pymongo import DESCENDING, PyMongo
import markdown
from datetime import datetime
from unicodedata import category
import uuid
from flask import Blueprint, redirect, render_template, request, session, url_for
from database import mongo
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import ValidationError
from bson.objectid import ObjectId

from forms.posts.CreatePostFrom import CreatePostForm

posts_page = Blueprint("posts_page", __name__, template_folder='templates')
POSTS_THEMES_FOLDER = './src/static/posts/'


@posts_page.route('')
def index():
    username = session['username'] if 'username' in session else ''
    posts = mongo.db.posts.find({'$or': [{"author": username, 'private': True}, {'private': False}]}).sort('created_at', DESCENDING)

    posts_dto = []
    for post in posts:
        theme_path = None
        if 'theme' in post and post['theme'] != None:
            theme_path= '/static/posts/' + post.get('theme')
        posts_dto.append({
            'id': post.get('_id'),
            'author': post.get('author'),
            'title': post.get('title'),
            'content': markdown.markdown(post.get('content')),
            'theme': theme_path
        })

    return render_template(f'pages/posts/index.html', posts = posts_dto)

@ posts_page.route('/create', methods=["GET", "POST"])
def create():
    if 'username' not in session:
        abort(403)

    form= CreatePostForm(request.form)

    username= session['username']
    if request.method == 'POST' and form.validate():
        ALLOWED_EXTENSIONS= {'png', 'jpg', 'jpeg'}
        image_id= None

        if request.files.__len__() > 0 and request.files[form.theme.name].filename != '':
            image_id= str(uuid.uuid4())
            theme_data= request.files[form.theme.name]
            filename= f'{username}_{image_id}{os.path.splitext(theme_data.filename)[1]}'
            folder= os.path.abspath(POSTS_THEMES_FOLDER)
            path= os.path.join(folder, filename)
            os.makedirs(folder, exist_ok=True)

            theme_data.save(path)

        result = mongo.db.posts.insert_one({
            "author": username,
            'created_at': datetime.now(),
            "title": form.title.data,
            "content": form.content.data,
            "private": form.private.data,
            "theme": filename if image_id else None
        })
        return redirect(url_for('posts_page.view', id=result.inserted_id))

    return render_template(f'pages/posts/create.html', form=form)

@ posts_page.route('<id>', methods=["GET", "POST"])
def view(id):
    post= mongo.db.posts.find_one(filter={"_id": ObjectId(id)})
    if post is None:
        abort(404)

    if post["private"] and session['username'] != post["author"]:
        abort(403)

    theme_path = None
    if 'theme' in post and post['theme'] != None:
        theme_path= '/static/posts/' + post.get('theme')

    data= {
        'id': post.get('_id'),
        'author': post.get('author'),
        'title': post.get('title'),
        'content': markdown.markdown(post.get('content')),
        'theme': theme_path
    }

    return render_template(f'pages/posts/view.html', data=data)
