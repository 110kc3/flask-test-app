from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField, FloatField
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



class AlgorithmResultsForm(FlaskForm):
    number_of_elements = IntegerField('number_of_elements')
    sorting_algorithm = StringField('sorting_algorithm')
    time_of_execution = FloatField('time_of_execution')

