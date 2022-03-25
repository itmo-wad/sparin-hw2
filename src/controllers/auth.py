from flask import Blueprint, redirect, render_template, request, session, url_for
from database import mongo
from forms.auth.SignInForm import SignInForm
from forms.auth.SignUpForm import SignUpForm
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import ValidationError

auth_page = Blueprint("auth_page", __name__, template_folder='templates')

@auth_page.route('/sign-in', methods=["GET", "POST"])
def sign_in():
    form = SignInForm(request.form)

    if request.method == 'GET':
        return render_template(f'pages/auth/sign-in.html', form=form)

    user = mongo.db.users.find_one(filter={ "username": form.username.data })
    if user == None or check_password_hash(user['password'], form.password.data) == False:
        form.username.errors+= (ValidationError(""),)
        form.password.errors+= (ValidationError("Invalid credentials"),)
        return render_template(f'pages/auth/sign-in.html', form=form, wrong_credentials=True)

    session['username'] = user['username']
        
    return redirect(url_for('index'))

@auth_page.route('/sign-up', methods=["GET", "POST"])
def sign_up():
    form = SignUpForm(request.form)
    if request.method == 'POST' and form.validate():
        
        userExists = mongo.db.users.find_one(filter={ "username": form.username.data })
        if userExists != None:
            form.username.errors.append("User is already exists")
            return render_template(f'pages/auth/sign-up.html', form=form)

        hashed_password = generate_password_hash(form.password.data)
        mongo.db.users.insert_one({"username": form.username.data, "password": hashed_password})
        return redirect(url_for('auth_page.sign_in'))

    return render_template(f'pages/auth/sign-up.html', form = form)

@auth_page.route('/sign-out')
def sign_out():
    session.pop('username', None)
    return redirect(url_for('index'))