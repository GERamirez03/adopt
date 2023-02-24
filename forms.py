"""WTForms for Adoption Agency."""

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, URLField, SelectField, BooleanField
from wtforms.validators import NumberRange, Optional, InputRequired

pets = ["dog", "cat", "porcupine"]

class AddPetForm(FlaskForm):
    """Form for adding pets to the adoption registry."""

    name = StringField('Name', validators=[InputRequired()])
    species = SelectField('Species', choices=[(pet, pet) for pet in pets])
    photo_url = URLField('Photo URL', validators=[Optional()])
    age = IntegerField('Age', validators=[Optional(), NumberRange(min=0,max=30)])
    notes = TextAreaField('Notes', validators=[Optional()])

class EditPetForm(FlaskForm):
    """Form for editing select pet information."""

    photo_url = URLField('Photo URL', validators=[Optional()])
    notes = TextAreaField('Notes', validators=[Optional()])
    available = BooleanField('Available for Adoption', validators=[Optional()])

    