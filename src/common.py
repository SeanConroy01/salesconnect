from models import Sale

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
