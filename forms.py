from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class EnrolCareer(FlaskForm):
    fullname = StringField("Full Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    tech_stack = StringField("Write your Teck Stack", validators=[DataRequired()])
    description = TextAreaField("Describe Your self", validators=[DataRequired()])
    submit = SubmitField("Submit")

class RegisterForm(FlaskForm):
    fullname = StringField("Full Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign Me Up!")