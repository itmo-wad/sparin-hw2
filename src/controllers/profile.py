from os import abort
from turtle import position
from flask import Blueprint, redirect, render_template, request, session, url_for, abort
from database import mongo
from wtforms import ValidationError

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
def edit():
    if 'username' not in session:
        abort(403)

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

    return render_template(f'pages/profile/edit.html', form=form)
