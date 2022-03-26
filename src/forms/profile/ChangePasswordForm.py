from wtforms import Form, BooleanField, StringField, PasswordField, validators


class ChangePasswordForm(Form):
    current = PasswordField(
        'Current password',
        [
            validators.InputRequired()
        ],
        render_kw={'type': "password", 'class': "form-control", 'id': "floatingPassword", 'placeholder': "Password"})
        
    password = PasswordField(
        'New password', [
            validators.InputRequired(),
            validators.EqualTo('confirm', message='Passwords must match')
        ],
        render_kw={'type': "password", 'class': "form-control", 'id': "floatingPassword", 'placeholder': "Password"})

    confirm = PasswordField(
        'Repeat new password',
        render_kw={'type': "password", 'class': "form-control", 'id': "floatingPassword", 'placeholder': "Password"})
