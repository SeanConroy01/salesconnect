from datetime import date
from flask import render_template, redirect, flash, url_for, Blueprint
from flask_login import login_required

from src.forms import CreateCustomerForm
from src.main import db, Customer
from src.common import calculate_customer_total, calculate_all_totals, format_number, admin_only

customer_routes = Blueprint('customer', __name__, template_folder='templates')

# Customer - All Customers
@customer_routes.route('/customer')
@login_required
def get_customers():
  customers = Customer.query.all()
  return render_template("customers.html", title="Customers", customers=calculate_all_totals(customers))

# Customer - Show Customer
@customer_routes.route("/customer/<int:customer_id>", methods=["GET"])
@login_required
def show_customer(customer_id):
  requested_customer = Customer.query.get(customer_id)
  return render_template("customer.html", title=requested_customer.name, customer=requested_customer, total_sales=format_number(calculate_customer_total(requested_customer.sales)))

# Customer - New Customer
@customer_routes.route("/new-customer", methods=["GET", "POST"])
@login_required
@admin_only
def new_customer():
  # Create form
  form = CreateCustomerForm()
  if form.validate_on_submit():
    # Create new customer object
    new_customer = Customer(
      name=form.name.data,
      industry=form.industry.data,
      date=date.today().strftime("%B %d, %Y")
    )
    #  Save customer
    db.session.add(new_customer)
    db.session.commit()
    # Log message to user
    flash("Customer has been Created.", "success")
    return redirect(url_for("customer.get_customers"))
  else:
    # Log error essage to user
    if form.errors:
        for error in form.errors.values():
          flash(error[0], "danger")
    return render_template("make-customer.html", title="New Customers", form=form)

# Customer - Edit Customer
@customer_routes.route("/edit-customer/<int:customer_id>", methods=["GET", "POST"])
@login_required
@admin_only
def edit_customer(customer_id):
  customer = Customer.query.get(customer_id)
  # Create form
  edit_form = CreateCustomerForm(
    name=customer.name,
    industry=customer.industry,
  )
  # Update customer data
  if edit_form.validate_on_submit():
    customer.name = edit_form.name.data
    customer.industry = edit_form.industry.data
    db.session.commit()
    # Log message to user
    flash("Customer has been updated.", "success")
    return redirect(url_for("customer.show_customer", customer_id=customer.id))
  else:
    # Log error essage to user
    if edit_form.errors:
        for error in edit_form.errors.values():
          flash(error[0], "danger")
    return render_template("make-customer.html", title="Edit Customers", form=edit_form, is_edit=True, customer_id=customer_id)

# Customer - Delete Customer
@customer_routes.route("/delete-customer/<int:customer_id>", methods=["GET"])
@login_required
@admin_only
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
  # Log message to user
  flash("Customer has been deleted.", "danger")
  return redirect(url_for('customer.get_customers'))
