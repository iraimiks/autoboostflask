from rapackege import db
from flask import (
    Blueprint, render_template, request
)
from rapackege.models import Customer, CustomerCars, ServiceCar

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

@ed.route('customer_car_service/<id>', methods=('GET', 'POST'))
def edit_car_service(id):
    servicecar = ServiceCar.query.get(id)
    if request.method == 'POST':
        service = request.form['service']
        partname = request.form['partname']
        spendtime = request.form['spendtime']
        worktype = request.form['worktype']

        servicecar.service = service
        servicecar.part_name = partname
        servicecar.spend_time = spendtime
        servicecar.work_type = worktype
        db.session.commit()
    return render_template("edit_forms/edit_car_service.html", servicecar=servicecar)
