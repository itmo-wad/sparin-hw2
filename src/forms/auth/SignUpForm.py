from wtforms import Form, BooleanField, StringField, PasswordField, validators


class SignUpForm(Form):
    username = StringField(
        'Username',
        [
            validators.Length(min=4, max=25),
            validators.InputRequired()
        ],
        render_kw={'class': 'form-control', 'id': 'floatingInput', 'placeholder': 'theblzh2017'})
        
    password = PasswordField(
        'Password', [
            validators.InputRequired(),
            validators.EqualTo('confirm', message='Passwords must match')
        ],
        render_kw={'type': "password", 'class': "form-control", 'id': "floatingPassword", 'placeholder': "Password"})

    confirm = PasswordField(
        'Repeat Password',
        render_kw={'type': "password", 'class': "form-control", 'id': "floatingPassword", 'placeholder': "Password"})
