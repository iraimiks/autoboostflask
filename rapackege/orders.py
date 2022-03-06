from rapackege import db
from flask import (
    Blueprint, render_template, request
)
from rapackege.models import Customer, CustomerCars, ServiceCar, CarServiceOrder, Users, OrdersCars

ord = Blueprint('order', __name__, url_prefix='/order')

@ord.route("/pre/<id>")
def order_prepare(id):
    car_service_order = CarServiceOrder.query.filter_by(id=id).first()
    service_of_car = ServiceCar.query.filter_by(id_orders_car=car_service_order.id_order).all()
    customer_car = CustomerCars.query.filter_by(id=car_service_order.customer_car_id).first()
    customer = Customer.query.filter_by(id=car_service_order.customer_id).first()
    worker = Users.query.filter_by(id=car_service_order.worker_id).first()
    order = OrdersCars.query.filter_by(id=car_service_order.id_order).first()
    print(service_of_car, customer_car, customer, worker, order)
    return render_template("work/prepare_order.html")