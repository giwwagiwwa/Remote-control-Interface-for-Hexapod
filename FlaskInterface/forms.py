from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Length(min=2,max=20)]) 
    #el Username es el nombre del campo y también para el HTML
    #limitaciones = validators: almenos dato DataRequired y num caracteres, )
    password = PasswordField('Password', validators = [DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrar')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Length(min=2,max=20)]) 
    #el Username es el nombre del campo y también para el HTML
    #limitaciones = validators: almenos dato DataRequired y num caracteres, )
    password = PasswordField('Password', validators = [DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')