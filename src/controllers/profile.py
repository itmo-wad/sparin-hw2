from os import abort
import os
from turtle import position
from flask import Blueprint, flash, redirect, render_template, request, session, url_for, abort
from database import mongo
from wtforms import ValidationError
from forms.profile.ChangeAvatarForm import ChangeAvatarForm
from forms.profile.ChangePasswordForm import ChangePasswordForm
from werkzeug.security import generate_password_hash, check_password_hash

from forms.profile.EditForm import EditForm

profile_page = Blueprint("profile_page", __name__, template_folder='templates')


@profile_page.route('/')
def index():
    if 'username' not in session:
        abort(403)

    user = mongo.db.users.find_one(filter={"username": session['username']})
    data = {
        'username': session['username'],
        'full_name': user.get('full_name', ''),
        'position': user.get('position', ''),
        'email': user.get('email', ''),
        'phone': user.get('phone', ''),
        'address': user.get('address', ''),
        'avatar_url': user.get('avatar_url', '/static/missing-avatar.png')
    }

    return render_template(f'pages/profile/index.html', data = data)


@profile_page.route('/edit', methods=['GET', 'POST'])
def edit(change_password_form = None, change_avatar_form = None):
    if 'username' not in session:
        abort(403)

    if change_password_form == None:
        change_password_form = ChangePasswordForm()

    if change_avatar_form == None:
        change_avatar_form = ChangeAvatarForm()

    user = mongo.db.users.find_one(filter={"username": session['username']})
    form = EditForm(request.form)

    if request.method == 'POST':
        if form.validate() == False:
            return render_template(f'pages/profile/edit.html', form=form)

        mongo.db.users.update_one({'username': session['username']}, {"$set": {
            'full_name': form.full_name.data,
            'position': form.position.data,
            'email': form.email.data,
            'phone': form.phone.data,
            'address': form.address.data,
        }})

        return redirect(url_for('profile_page.index'))

    form.full_name.data = user.get('full_name', '')
    form.position.data = user.get('position', '')
    form.email.data = user.get('email', '')
    form.phone.data = user.get('phone', '')
    form.address.data = user.get('address', '')

    return render_template(f'pages/profile/edit.html', form = form, change_password_form = change_password_form, change_avatar_form = change_avatar_form)

# I'm lazy, don't bite me
@profile_page.route('/avatar', methods=['POST'])
def change_avatar():
    if 'username' not in session:
        abort(403)

    username = session['username']
    form = ChangeAvatarForm(request.form)

    AVATARS_FOLDER = './src/static/avatars/'    
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

    if request.files.__len__() > 0:
        avatar_data = request.files[form.avatar.name]
        filename = f'{username}{os.path.splitext(avatar_data.filename)[1]}'

        folder = os.path.abspath(AVATARS_FOLDER)
        path = os.path.join(folder, filename)
        os.makedirs(folder, exist_ok=True)

        avatar_data.save(path)

        mongo.db.users.update_one({'username': session['username']}, {"$set": {
            'avatar_url': f'/static/avatars/{filename}',
        }})
    else:
        return edit(change_avatar_form=form)

    return index()

# I'm lazy, don't bite me
@profile_page.route('/password', methods=['POST'])
def change_password():
    if 'username' not in session:
        abort(403)

    form = ChangePasswordForm(request.form)

    user = mongo.db.users.find_one(filter={ "username": session['username'] })
    if user == None or check_password_hash(user['password'], form.current.data) == False:
        form.current.errors+= (ValidationError("Invalid password"),)
        flash("Invalid password")
        return redirect(url_for('profile_page.edit'))

    if form.validate():
        hashed_password = generate_password_hash(form.password.data)
        mongo.db.users.update_one({'username': session['username']}, {"$set": {
            'password': hashed_password,
        }})
    else:    
        flash("New password doesn't match")
        return redirect(url_for('profile_page.edit'))

    return redirect(url_for('profile_page.index'))

