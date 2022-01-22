from rapackege import app, db
from flask import (
    g, redirect, render_template, request, url_for
)
from rapackege.validation import validate_Customer_car
from rapackege.auth import login_required, admin_role
from rapackege.models import (
    OrdersCars, Customer, CustomerCars, ServiceCar, Users, WorkersCar, CarServiceOrder
)
from sqlalchemy import desc
from sqlalchemy.sql import functions
from flask_weasyprint import HTML, render_pdf

import datetime

@app.route("/order_p/<idorder>")
@login_required
def order_p(idorder):
    today = datetime.datetime.now()
    date_time = today.strftime("%d/%m/%Y")
    order_items = ServiceCar.query.filter_by(id_orders_car=idorder).all()
    html = render_template("pdf/order_pdf.html", date_time=date_time, order_items=order_items)
    return render_pdf(HTML(string=html))


@app.route("/")
@app.route("/home")
def home_page():
    return render_template("home_page.html")

@app.context_processor
def inject_user():
    return dict(user=g.user)


@app.route("/customer_reg", methods=('GET', 'POST'))
@login_required
@admin_role
def customer_reg():
    customerexist = None
    if request.method == 'POST':
        phone_number = request.form['phonenumber']
        name = request.form['customername']
        new_customer = Customer(
            phone_number=phone_number,
            name=name,
            create_date=datetime.datetime.now()
        )
        customer = Customer.query.filter_by(phone_number=phone_number).first()
        if customer is None:
            db.session.add(new_customer)
            db.session.commit()
            customer = Customer.query.order_by(desc("id")).first()
            return redirect(url_for('customer_cars',id=customer.id))
        else:
            customerexist = "Šis lietotājs eksistē"
    return render_template("work/customer_reg.html",customerexist=customerexist)


@app.route("/customers", methods=('GET', 'POST'))
@login_required
@admin_role
def all_customers():
    customers = Customer.query.order_by(desc("id")).all()
    return render_template("work/customers.html", customers=customers)

@app.route("/customer/<id>", methods=('GET', 'POST'))
@login_required
@admin_role
def customer_cars(id):
    customer = Customer.query.filter_by(id=id).first()
    customer_cars = CustomerCars.query.filter_by(customer_id=customer.id).all()
    carexist = None
    if request.method == 'POST':
        car_name = request.form['car_name']
        new_customercar = CustomerCars(
            car_name = car_name,
            create_date = datetime.datetime.now(),
            customer_id = customer.id
        )
        customercar = CustomerCars.query.filter_by(car_name=car_name).first()
        if customercar is None:
            db.session.add(new_customercar)
            db.session.commit()
            return redirect(url_for('customer_cars',id=id))
        else:
            carexist = validate_Customer_car(car_name)
    return render_template("work/customer_cars.html", customer=customer, customer_cars=customer_cars, carexist=carexist)

@app.route("/customer_car_service/<id>", methods=('GET', 'POST'))
@login_required
def customer_car_service(id):
    id_orders_car = OrdersCars.query.filter_by(id=id).first()
    app.logger.info(id_orders_car.order_status)
    car = CustomerCars.query.filter_by(id=id_orders_car.id_car).first()
    customer = Customer.query.filter_by(id=car.customer_id).first()
    service_cars = ServiceCar.query.filter_by(id_orders_car=id_orders_car.id).all()
    worker = Users.query.filter_by(id=id_orders_car.id_user).first()
    if request.method == 'POST':
        service = request.form['service']
        partname = request.form['partname']
        spendtime = request.form['spendtime']
        worktype = request.form['worktype']
        regwork = ServiceCar(
            service = service,
            part_name = partname,
            spend_time = spendtime,
            work_type = worktype,
            car_id = car.id,
            id_orders_car = id_orders_car.id,
            create_date = datetime.datetime.now()
        )
        db.session.add(regwork)
        db.session.commit()
        return redirect(url_for('customer_car_service',id=id_orders_car.id))
    return render_template("work/customer_car_service.html", car=car, customer=customer, service_cars=service_cars, worker=worker, id_orders_car=id_orders_car)

@app.route("/car_to_worker", methods=('GET', 'POST'))
@login_required
@admin_role
def car_to_worker():
    if request.method == 'POST':
        carid = request.form['carid']
        workerid = request.form.get('workerid')
        customerid = request.form['customerid']
        worker_cars = WorkersCar(
            customer_car_id = carid,
            worker_id = workerid,
            car_work_status = "darbs pie auto"
        )
        db.session.add(worker_cars)
        db.session.commit()
        return redirect(url_for('customer_cars',id=customerid))

def worker_cars(id):
    worker_orders = OrdersCars.query.filter_by(id_user=id).all()
    worker = Users.query.filter_by(id=id).first()
    return render_template("work/worker_work.html",worker_orders=worker_orders, worker=worker)

app.add_url_rule('/worker_cars/<id>','worker_cars',worker_cars)

#Prepare order
@app.route("/order_pre", methods=('GET', 'POST'))
def order_pre():
    if request.method == 'POST':
        customercarid = request.form['customercarid']
        customerid = request.form['customerid']
        orderid = request.form['orderid']
        order_for_car = CarServiceOrder(
            customer_car_id = customercarid, 
            worker_id = g.user.id,
            customer_id = customerid,
            id_order = orderid,
            car_work_satus = 'done', 
            order_status = 'gaida apmaksu',
            create_date = datetime.datetime.now()
        )
        db.session.add(order_for_car)
        order = OrdersCars.query.get(orderid)
        spendtime = (db.session.query(functions.sum(ServiceCar.spend_time))\
        .filter(ServiceCar.id_orders_car == orderid))
        order.spend_time = spendtime
        order.order_status = 'darbs izdarīts'
        db.session.commit()
        return redirect(url_for('customer_car_service',id=orderid))

@app.route("/all_orders", methods=('GET', 'POST'))
@admin_role
@login_required
def all_orders():
    order_details = (db.session.query(CarServiceOrder, Customer, CustomerCars)\
    .filter(CarServiceOrder.customer_id == Customer.id)\
    .filter(CarServiceOrder.customer_car_id == CustomerCars.id).order_by(desc(CarServiceOrder.id_order)).all())
    return render_template("work/all_orders.html", order_details=order_details)

@app.route("/car_orders/<id>", methods=('GET', 'POST'))
@login_required
@admin_role
def car_orders(id):
    workers = Users.query.order_by(desc("id")).all()
    id_car = CustomerCars.query.filter_by(id=id).first()
    orders = OrdersCars.query.filter_by(id_car=id_car.id).all()
    car = CustomerCars.query.filter_by(id=id).first()
    if request.method == 'POST':
        date_as_id = datetime.datetime.now().strftime('%Y%m%d%H%M')
        workerid = request.form.get('workerid')
        worker = Users.query.filter_by(id=workerid).first()
        create_order = OrdersCars(
            order_name=car.car_name+"_"+date_as_id,
            order_status="darbs sākts",
            id_car=id,
            id_user = workerid,
            worker_name = worker.username,
            spend_time = None,
            create_date = datetime.datetime.now()
        )
        worker_cars = WorkersCar(
            customer_car_id = id,
            worker_id = workerid,
            car_work_status = "darbs pie auto"
        )
        db.session.add(worker_cars)
        db.session.add(create_order)
        db.session.commit()
        return redirect(url_for('car_orders',id=id))
    return render_template("work/car_orders.html",orders=orders,workers=workers,car=car)


@app.route("/all_workers")
@login_required
@admin_role
def all_workers():
    workers = Users.query.order_by(desc("id")).all()
    return render_template("admin_dashboard/all_workers.html",workers=workers)