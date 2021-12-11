from rapackege import db
from werkzeug.security import generate_password_hash

class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    phone_number = db.Column(db.String(length=30))
    name = db.Column(db.String(length=30))
    create_date = db.Column(db.DateTime)
    def __init__(self, phone_number, name, create_date):
        self.phone_number = phone_number
        self.name = name
        self.create_date = create_date

class CustomerCars(db.Model):
    __tablename__ = 'customer_cars'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    car_name = db.Column(db.String(length=30))
    create_date = db.Column(db.DateTime)
    customer_id = db.Column(db.Integer(), db.ForeignKey('customers.id'), nullable=False)
    def __init__(self, car_name, create_date, customer_id):
        self.car_name = car_name
        self.create_date = create_date
        self.customer_id = customer_id

class ServiceCar(db.Model):
    __tablename__ = 'service_cars'
    id  = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    service = db.Column(db.String(length=30))
    part_name = db.Column(db.String(length=30))
    spend_time = db.Column(db.Integer())
    work_type = db.Column(db.String(length=30))
    car_id = db.Column(db.Integer())
    create_date = db.Column(db.DateTime)
    id_orders_car = db.Column(db.Integer(), db.ForeignKey('orders_cars.id'), nullable=False)
    def __init__(self, service, part_name, spend_time, work_type, car_id, id_orders_car, create_date):
        self.service = service
        self.part_name = part_name
        self.spend_time = spend_time
        self.work_type = work_type
        self.car_id = car_id
        self.id_orders_car = id_orders_car
        self.create_date = create_date

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_role = db.Column(db.String(length=30))
    username = db.Column(db.String(length=30))
    password = db.Column(db.String(128))
    def __init__(self, user_role, username, password):
        self.user_role = user_role
        self.username = username
        self.password = generate_password_hash(password)

class WorkersCar(db.Model):
    __tablename__ = 'on_work_cars'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_car_id = db.Column(db.Integer())
    worker_id = db.Column(db.Integer())
    car_work_status = db.Column(db.String(length=30))
    def __init__(self, customer_car_id, worker_id, car_work_status):
        self.customer_car_id = customer_car_id
        self.worker_id = worker_id
        self.car_work_status = car_work_status

class CarServiceOrder(db.Model):
    __tablename__ = 'car_service_order'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_car_id = db.Column(db.Integer())
    worker_id = db.Column(db.Integer())
    customer_id = db.Column(db.Integer())
    id_order = db.Column(db.Integer())
    car_work_status = db.Column(db.String(length=30))
    order_status = db.Column(db.String(length=30))
    create_date = db.Column(db.DateTime)
    def __init__(self, customer_car_id, worker_id, customer_id, id_order, car_work_satus, order_status, create_date):
        self.customer_car_id = customer_car_id
        self.worker_id = worker_id
        self.customer_id = customer_id
        self.id_order = id_order
        self.car_work_status = car_work_satus
        self.order_status = order_status
        self.create_date = create_date

class OrdersCars(db.Model):
    __tablename__ = 'orders_cars'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_name = db.Column(db.String(length=30))
    order_status = db.Column(db.String(length=30))
    spend_time = db.Column(db.String(length=30))
    create_date = db.Column(db.DateTime)
    id_car = db.Column(db.Integer(), db.ForeignKey('customer_cars.id'), nullable=False)
    id_user = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable=False)
    worker_name = db.Column(db.String(length=30))
    def __init__(self, order_name, order_status, id_car, id_user, spend_time, create_date, worker_name):
        self.order_name = order_name
        self.order_status = order_status
        self.id_car = id_car 
        self.id_user = id_user
        self.worker_name = worker_name
        self.spend_time = spend_time
        self.create_date = create_date