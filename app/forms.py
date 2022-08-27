from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired

class UserForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired()])


class EncryptionForm(FlaskForm):
    key = StringField('key', validators=[InputRequired()])
    text_to_encrypt = StringField('text_to_encrypt')
    text_to_decrypt = StringField('text_to_decrypt')
