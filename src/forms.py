from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length

## WTForm
class CreateCustomerForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    industry = StringField("Industry", validators=[DataRequired()])

class LoginForm(FlaskForm):
  email = StringField(label='Email', validators=[DataRequired()])
  password = PasswordField(label='Password', validators=[DataRequired(), Length(min=8)])

class RegisterForm(FlaskForm):
  name = StringField("Name", validators=[DataRequired()])
  email = StringField(label='Email', validators=[DataRequired()])
  role = StringField(label='Role', validators=[DataRequired()])
  password = PasswordField(label='Password', validators=[DataRequired(), Length(min=8)])

class ChangePasswordForm(FlaskForm):
  current_password = PasswordField(label='Current Password', validators=[DataRequired()])
  new_password = PasswordField(label='New Password', validators=[DataRequired(), Length(min=8)])
  confirm_password = PasswordField(label='Confirm Password', validators=[DataRequired(), Length(min=8)])