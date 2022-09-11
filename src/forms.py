from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, PasswordField, SelectField
from wtforms.validators import DataRequired, Length, Email

## WTForm
class LoginForm(FlaskForm):
  email = StringField(label='Email', validators=[DataRequired(), Email()])
  password = PasswordField(label='Password', validators=[DataRequired()])

class RegisterForm(FlaskForm):
  name = StringField("Name", validators=[DataRequired()])
  email = StringField(label='Email', validators=[DataRequired(), Email()])
  role = SelectField("Role", choices=["user", "admin"], validators=[DataRequired()])
  password = PasswordField(label='Password', validators=[DataRequired(), Length(min=8, max=40)])

class ChangePasswordForm(FlaskForm):
  current_password = PasswordField(label='Current Password', validators=[DataRequired()])
  new_password = PasswordField(label='New Password', validators=[DataRequired(), Length(min=8, max=40)])
  confirm_password = PasswordField(label='Confirm Password', validators=[DataRequired(), Length(min=8, max=40)])

class CreateCustomerForm(FlaskForm):
  name = StringField("Name", validators=[DataRequired()])
  industry = StringField("Industry", validators=[DataRequired()])

class CreateContactForm(FlaskForm):
  name = StringField("Name", validators=[DataRequired()])
  email = StringField(label='Email', validators=[DataRequired(), Email()])
  role = StringField(label='Role', validators=[DataRequired()])
  phone = StringField(label='Phone Number', validators=[DataRequired()])

class CreateSaleForm(FlaskForm):
  value = DecimalField("Value", places=2, rounding=None, validators=[DataRequired()])
  reference = StringField(label='Reference', validators=[DataRequired()])
  status = SelectField("Status", choices=["Pending", "Shipped", "Arrived","Installed", "Complete"], validators=[DataRequired()])