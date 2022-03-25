from wtforms import Form, BooleanField, StringField, PasswordField, validators

class SignInForm(Form):
    username = StringField(
        'Username',
        [
            validators.InputRequired()
        ],
        render_kw={'class': 'form-control', 'id': 'floatingInput', 'placeholder': 'theblzh2017'})
        
    password = PasswordField(
        'Password', [
            validators.InputRequired()
        ],
        render_kw={'type': "password", 'class': "form-control", 'id': "floatingPassword", 'placeholder': "Password"})