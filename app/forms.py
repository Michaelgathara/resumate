from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, Email

class ResumeForm(FlaskForm):
    user_id = IntegerField('User ID', validators=[DataRequired()])
    content = TextAreaField('Resume Content', validators=[DataRequired(), Length(min=10)])
    submit = SubmitField('Submit Resume')

class JobPostingForm(FlaskForm):
    title = StringField('Job Title', validators=[DataRequired(), Length(min=1, max=100)])
    description = TextAreaField('Job Description', validators=[DataRequired(), Length(min=10)])
    submit = SubmitField('Submit Job')