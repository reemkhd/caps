from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, DateTimeField
#, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, AnyOf, URL, InputRequired


class MovieForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    relase_date = DateTimeField(
        'relase_date',
        default= datetime.today()
    )