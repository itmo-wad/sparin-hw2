from flask import Flask, redirect, render_template, session, url_for
from database import mongo
from flask_pymongo import PyMongo
from controllers.auth import auth_page
import controllers.auth

app = Flask(__name__)
app.config['SECRET_KEY'] = 'the random string'
app.config["MONGO_URI"] = "mongodb://localhost:27017/hw-2"

mongo.init_app(app)

app.register_blueprint(auth_page, url_prefix='/auth')

@app.route("/")
def index():
    if 'username' in session:
        return render_template(f'pages/index.html')

    # Render authentication form at http://localhost:5000/
    return redirect(url_for("auth_page.sign_in"))

if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)