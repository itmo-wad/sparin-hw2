from wtforms import Form, BooleanField, StringField, PasswordField, validators, FileField

class ChangeAvatarForm(Form):
    avatar = FileField(
        'Avatar',
        [
            validators.DataRequired()
        ],
        render_kw={ 'accept': '.png,.jpg,.jpeg'})