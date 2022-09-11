from flask import render_template, Blueprint
from flask_login import login_required

home_routes = Blueprint('home', __name__, template_folder='templates')

# Home - Show Home
@home_routes.route('/')
@login_required
def home():
   return render_template("index.html", title="Home")