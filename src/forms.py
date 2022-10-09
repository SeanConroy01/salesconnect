from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, PasswordField, SelectField
from wtforms.validators import DataRequired, Length, Email, Regexp

## WTForm
class LoginForm(FlaskForm):
  email = StringField(label='Email', validators=[DataRequired()])
  password = PasswordField(label='Password', validators=[DataRequired()])

class RegisterForm(FlaskForm):
  name = StringField("Name", validators=[DataRequired(), Regexp('[A-Za-z]', message="Name must only contain letters.")])
  email = StringField(label='Email', validators=[DataRequired(), Email("Email must be a valid email address")])
  role = SelectField("Role", choices=["user", "admin"], validators=[DataRequired(), Regexp('[A-Za-z]', message="Name must only contain letters.")])
  password = PasswordField(label='Password', validators=[DataRequired(), Length(min=8, max=40)])

class ChangePasswordForm(FlaskForm):
  current_password = PasswordField(label='Current Password', validators=[DataRequired()])
  new_password = PasswordField(label='New Password', validators=[DataRequired(), Length(min=8, max=40)])
  confirm_password = PasswordField(label='Confirm Password', validators=[DataRequired(), Length(min=8, max=40)])

class CreateCustomerForm(FlaskForm):
  name = StringField("Name", validators=[DataRequired(), Regexp('[A-Za-z0-9]', message="Name must only contain letters and numbers.")])
  industry = StringField("Industry", validators=[DataRequired(), Regexp('[A-Za-z]', message="Industry must only contain letters.")])

class CreateContactForm(FlaskForm):
  name = StringField("Name", validators=[DataRequired(), Regexp('[A-Za-z]', message="Name must only contain letters.")])
  email = StringField(label='Email', validators=[DataRequired(), Email("Email must be a valid email address")])
  role = StringField(label='Role', validators=[DataRequired(), Regexp('[A-Za-z]', message="Name must only contain letters.")])
  phone = StringField(label='Phone Number', validators=[DataRequired(), Regexp('[0-9]', message="Phone number must only contain numbers.")])

class CreateSaleForm(FlaskForm):
  value = DecimalField("Value", places=2, rounding=None, validators=[DataRequired()])
  status = SelectField("Status", choices=["Pending", "Shipped", "Arrived","Installed", "Complete"], validators=[DataRequired()])
