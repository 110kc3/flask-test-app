from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired

class UserForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired()])


class SortForm(FlaskForm):
    table_to_sort = StringField('key')



class EncryptionForm(FlaskForm):
    key = StringField('key')
    text_to_encrypt = StringField('text_to_encrypt')
    text_to_decrypt = StringField('text_to_decrypt')
