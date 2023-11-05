#for creating forms we need many different validation checks, some reg-ex for valid email, check password etc. For this is an extension wtforms which makes all these things easy.We will be writing python classes representing forms, they will be converted to html forms in templates

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired,Length,Email,EqualTo

class RegistrationForm(FlaskForm): # use of inheritance, RegistratonForm(child class) inheriting from FlaskForm(parent class)  
  username = StringField('Username',validators=[DataRequired(),Length(min = 2,max = 20)]) #first argument is the name of the field and it will also be used as a label in out html. 
  email = StringField('Email', validators=[DataRequired(),Email()])
  password = PasswordField("Password",validators=[DataRequired()])
  confirm_password = PasswordField("Password",validators=[DataRequired(),EqualTo('password')])
  submit = SubmitField('Sign Up') #Sign up is the label


class LoginForm(FlaskForm):
  email = StringField('Email', validators=[DataRequired(),Email()])
  password = PasswordField("Password",validators=[DataRequired()])
  remember = BooleanField('Remember Me')
  submit = SubmitField('Log In')