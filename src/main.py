import os
from flask import Flask, redirect, render_template, url_for
from flask_login import LoginManager
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

from models import db, User
from routes.auth import auth_routes
from routes.home import home_routes
from routes.customer import customer_routes
from routes.sale import sale_routes
from routes.contact import contact_routes

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

## Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@login_manager.unauthorized_handler
def unauthorized():
  return redirect(url_for("auth.login"))

db.create_all()

app.register_blueprint(auth_routes)
app.register_blueprint(home_routes)
app.register_blueprint(customer_routes)
app.register_blueprint(sale_routes)
app.register_blueprint(contact_routes)

# Error Handlers
@app.errorhandler(404)
def page_not_found(e):
 return render_template('errors/404.html', title="Page Not Found"), 404

@app.errorhandler(500)
def internal_server_error(e):
  return render_template('errors/500.html', title="Something Went Wrong"), 500

@app.errorhandler(403)
def page_forbidden(e):
  return redirect('/')

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True, port=os.getenv('PORT'))