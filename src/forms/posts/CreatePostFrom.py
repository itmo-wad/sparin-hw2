from wtforms import Form, BooleanField, StringField, PasswordField, validators, FileField, TextAreaField

class CreatePostForm(Form):
    title = StringField(
        'Title',
        [
            validators.InputRequired()
        ],
        render_kw={'class': 'form-control', 'placeholder': 'Homework #3'})

    content = TextAreaField(
        'Content',
        [
            validators.InputRequired()
        ],
        render_kw={'class': 'form-control', 'placeholder': 'Put your README file here', "rows": 5})

    private = BooleanField(
        'Private',
        [

        ],
        render_kw={'class': 'form-check-input'})

    theme = FileField(
        'Theme',
        [

        ],
        render_kw={ 'accept': '.png,.jpg,.jpeg'})