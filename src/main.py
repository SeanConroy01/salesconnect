import os
from flask import Flask, redirect, render_template, url_for
from flask_login import LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from dotenv import load_dotenv

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

class User(UserMixin, db.Model):
  __tablename__ = "users"
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(100), unique=True)
  password = db.Column(db.String(100))
  name = db.Column(db.String(100))
  role = db.Column(db.String(100), default="user")
  sales = relationship("Sale", back_populates="rep")

class Customer(db.Model):
  __tablename__ = "customers"
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(250), unique=True, nullable=False)
  industry = db.Column(db.String(250), nullable=False)
  date = db.Column(db.String(250), nullable=False)
  contacts = relationship("Contact", back_populates="parent_customer")
  sales = relationship("Sale", back_populates="parent_customer")

class Contact(db.Model):
  __tablename__ = "contacts"
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100))
  email = db.Column(db.String(100))
  role = db.Column(db.String(100))
  phone = db.Column(db.String(100))
  customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"))
  parent_customer = relationship("Customer", back_populates="contacts")

class Sale(db.Model):
  __tablename__ = "sales"
  id = db.Column(db.Integer, primary_key=True)
  rep_id = db.Column(db.Integer, db.ForeignKey("users.id"))
  rep = relationship("User", back_populates="sales")
  value = db.Column(db.Float())
  date = db.Column(db.String(250))
  status = db.Column(db.String(100))
  customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"))
  parent_customer = relationship("Customer", back_populates="sales")

db.create_all()

from src.routes.auth import auth_routes
from src.routes.home import home_routes
from src.routes.customer import customer_routes
from src.routes.sale import sale_routes
from src.routes.contact import contact_routes

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

