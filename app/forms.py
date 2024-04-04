# Add any form classes for Flask-WTF here
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import InputRequired

class MovieForm(FlaskForm):
    # Text Field
    title = StringField('Property Title', validators=[InputRequired()])

    # Text Are Fiekd
    description = TextAreaField('Description', validators=[InputRequired()])

    # File Upload
    photo = FileField('Photo', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])