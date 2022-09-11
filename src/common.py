from functools import wraps
from flask import abort
from flask_login import current_user

from src.main import Sale

def admin_only(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
      if current_user.role != 'admin':
          return abort(403)
      return f(*args, **kwargs)
  return decorated_function

def get_related_sales(current_user):
  if current_user.role == "admin":
    return Sale.query.all()
  else:
    return current_user.sales

def calculate_customer_total(sales):
  total_sales = 0
  for sale in sales:
    total_sales += sale.value
  return total_sales

def calculate_all_totals(customers):
  for customer in customers:
      customer.value = calculate_customer_total(customer.sales)
  return customers

def format_number(number):
  return "{:,}".format(number)
