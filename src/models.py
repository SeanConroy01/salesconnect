from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin

db = SQLAlchemy()

## Configure Tables
class User(UserMixin, db.Model):
  __tablename__ = "users"
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(100), unique=True)
  password = db.Column(db.String(100))
  name = db.Column(db.String(100))
  role = db.Column(db.String(100), default="user")

class Customer(db.Model):
  __tablename__ = "customers"
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(250), unique=True, nullable=False)
  industry = db.Column(db.String(250), nullable=False)
  date = db.Column(db.String(250), nullable=False)
  contacts = relationship("Contact", back_populates="parent_customer")

class Contact(db.Model):
  __tablename__ = "contacts"
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100))
  email = db.Column(db.String(100))
  role = db.Column(db.String(100))
  phone = db.Column(db.String(100))
  customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"))
  parent_customer = relationship("Customer", back_populates="contacts")