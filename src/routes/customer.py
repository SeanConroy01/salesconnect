from datetime import date
from flask import render_template, redirect, flash, url_for, Blueprint
from flask_login import login_required
from forms import CreateCustomerForm
from models import db, Customer

customer_routes = Blueprint('customer', __name__, template_folder='templates')

# Customer - All Customers
@customer_routes.route('/customer')
@login_required
def get_customers():
  customers = Customer.query.all()
  for customer in customers:
    customer.value = 0
    for sale in customer.sales:
      customer.value += sale.value
  return render_template("customers.html", title="Customers", customers=customers)

# Customer - Show Customer
@customer_routes.route("/customer/<int:customer_id>", methods=["GET"])
@login_required
def show_customer(customer_id):
  requested_customer = Customer.query.get(customer_id)
  total_sales = 0
  for sale in requested_customer.sales:
    total_sales += sale.value
  return render_template("customer.html", title=requested_customer.name, customer=requested_customer, total_sales="{:,}".format(total_sales))

# Customer - New Customer
@customer_routes.route("/new-customer", methods=["GET", "POST"])
@login_required
def new_customer():
  form = CreateCustomerForm()
  if form.validate_on_submit():
    new_customer = Customer(
      name=form.name.data,
      industry=form.industry.data,
      date=date.today().strftime("%B %d, %Y")
    )
    db.session.add(new_customer)
    db.session.commit()
    flash("Customer has been Created.", "success")
    return redirect(url_for("customer.get_customers"))
  return render_template("make-customer.html", title="New Customers", form=form)

# Customer - Edit Customer
@customer_routes.route("/edit-customer/<int:customer_id>", methods=["GET", "POST"])
@login_required
def edit_customer(customer_id):
  customer = Customer.query.get(customer_id)
  edit_form = CreateCustomerForm(
    name=customer.name,
    industry=customer.industry,
  )
  if edit_form.validate_on_submit():
    customer.name = edit_form.name.data
    customer.industry = edit_form.industry.data
    db.session.commit()
    flash("Customer has been updated.", "success")
    return redirect(url_for("customer.show_customer", customer_id=customer.id))
  return render_template("make-customer.html", title="Edit Customers", form=edit_form, is_edit=True, customer_id=customer_id)

# Customer - Delete Customer
@customer_routes.route("/delete-customer<int:customer_id>", methods=["GET"])
@login_required
def delete_customer(customer_id):
  customer_to_delete = Customer.query.get(customer_id)
  # Delete linked sales
  for sale in customer_to_delete.sales:
    db.session.delete(sale)
  # Delete linked contacts
  for contact in customer_to_delete.contacts:
    db.session.delete(contact)
  # Delete customer
  db.session.delete(customer_to_delete)
  db.session.commit()
  flash("Customer has been delelted.", "danger")
  return redirect(url_for('customer.get_customers'))
