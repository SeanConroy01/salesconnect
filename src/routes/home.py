import json
from flask import render_template, Blueprint
from flask_login import login_required, current_user

from src.common import get_related_sales, calculate_customer_total, format_number

home_routes = Blueprint('home', __name__, template_folder='templates')

# Home - Show Home
@home_routes.route('/')
@login_required
def home():
  customers = {}
  reps = {}
  sales = get_related_sales(current_user)
  total = calculate_customer_total(sales)

  highest = 0
  for sale in sales:
    if sale.value > highest:
      highest = sale.value
    
    if sale.parent_customer.name in customers:
      customers[sale.parent_customer.name] += sale.value
    else:
      customers[sale.parent_customer.name] = sale.value

    if sale.rep.name in reps:
      reps[sale.rep.name] += sale.value
    else:
      reps[sale.rep.name] = sale.value

  data = {
    "total": format_number(total),
    "highest": format_number(highest),
    "num": len(sales),
  }

  chart_data = {
    "customer_name": list(customers.keys()),
    "customer_value": list(customers.values()),
    "customer_value_per": [round(value / total * 100, 2) for value in list(customers.values())],
    "rep_name": list(reps.keys()),
    "rep_value": list(reps.values()),
    "rep_value_per": [round(value / total * 100, 2) for value in list(reps.values())],
  }

  return render_template("index.html", title="Home", data=data, chart_data=json.dumps(chart_data))