from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

## Configure Tables
class Customer(db.Model):
  __tablename__ = "customers"
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(250), unique=True, nullable=False)
  industry = db.Column(db.String(250), nullable=False)
  date = db.Column(db.String(250), nullable=False)