from flask_wtf import FlaskForm, Form
from wtforms import StringField, SelectField, SubmitField

#
# class POIForm(FlaskForm):
#     name = StringField('Appellation')
#     city = StringField('Ville')
#     search = SubmitField('Rechercher')


class Search(Form):
    choices = [('Appellation', 'Appellation'),
               ('Ville', 'Ville')]
    select = SelectField('Rechercher un lieu :', choices=choices)
    search = StringField('')

