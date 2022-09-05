from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField
from wtforms.validators import DataRequired

## WTForm
class CreateCustomerForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    industry = StringField("Industry", validators=[DataRequired()])