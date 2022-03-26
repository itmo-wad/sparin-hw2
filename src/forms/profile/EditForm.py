from wtforms import Form, BooleanField, StringField, PasswordField, validators, EmailField


class EditForm(Form):
    full_name = StringField(
        'Full Name',
        [
            validators.InputRequired()
        ],
        render_kw={'class': 'form-control', 'id': 'fullNameInput', 'placeholder': 'Ivan Ivanovich'})
        
    position = StringField(
        'Position', [
            validators.InputRequired()
        ],
        render_kw={ 'class': "form-control", 'placeholder': "Web Developer"})

    email = EmailField(
        "Email",
        render_kw={ 'class': "form-control", 'placeholder': "email@example.com"}
    )

    phone = StringField(
        "Phone",
        render_kw={ 'class': "form-control", 'placeholder': "8 (800) 555-35-35"}
    )

    address = StringField(
        'Address',
        render_kw={ 'class': "form-control", 'placeholder': "Saint-Petersburg, Russia"})
