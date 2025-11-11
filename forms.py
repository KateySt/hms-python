from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateTimeLocalField
from wtforms.validators import DataRequired, Length


class EventForm(FlaskForm):
    title = StringField('Event Title', validators=[DataRequired(), Length(max=20)])
    description = TextAreaField('Event Description', validators=[Length(max=500)])
    date = DateTimeLocalField('Event Date',format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
