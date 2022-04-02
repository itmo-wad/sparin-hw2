import os
from flask import Flask, redirect, render_template, session, url_for
from database import mongo
from flask_pymongo import PyMongo
from controllers.auth import auth_page
from controllers.profile import profile_page
from controllers.posts import posts_page
from controllers.cards import cards_page
import controllers.auth

app = Flask(__name__)
app.config['SECRET_KEY'] = 'the random string'
app.config["MONGO_URI"] = os.environ.get("DB_CONNECTION_STRING", "mongodb://localhost:27017/hw-2")

AVATARS_PATH = './src/static/avatars/'

mongo.init_app(app)

app.register_blueprint(auth_page, url_prefix='/auth')
app.register_blueprint(profile_page, url_prefix='/profile')
app.register_blueprint(posts_page, url_prefix='/posts')
app.register_blueprint(cards_page, url_prefix='/cards')

@app.route("/")
def index():
    if 'username' in session:
        return render_template(f'pages/index.html')

    # Render authentication form at http://localhost:5000/
    return redirect(url_for("auth_page.sign_in"))

if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)