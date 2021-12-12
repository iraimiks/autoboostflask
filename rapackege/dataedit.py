from rapackege import app,db
import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from rapackege.models import Customer, CustomerCars

ed = Blueprint('edit', __name__, url_prefix='/edit')

@ed.route('/customer/<id>', methods=('GET', 'POST'))
def edit_customers(id):
    customer = Customer.query.get(id)
    if request.method == 'POST':
        phonenumber = request.form['phonenumber']
        name = request.form['name']

        customer.phone_number = phonenumber
        customer.name = name
        db.session.commit()
    return render_template("edit_forms/edit_customer.html",customer=customer)


@ed.route('customer_car/<id>', methods=('GET', 'POST'))
def edit_customer_car(id):
    customercar = CustomerCars.query.get(id)
    if request.method == 'POST':
        carname = request.form['carname']

        customercar.car_name = carname
        db.session.commit()
    return render_template("edit_forms/edit_customer_car.html", customercar=customercar)