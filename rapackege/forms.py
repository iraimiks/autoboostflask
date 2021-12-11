from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField


class RegWorkDoneForCar(FlaskForm):
    work_action = RadioField(label='workaction',choices=[(1, 'diagnostika'),(2,'remonts')],default=1, coerce=int)
    car_number = StringField(label='carnumber')
    phonenumber = StringField(label='phonenumber')
    customer_name = StringField(label='customername')
    work_name = StringField(label='workname')
    part_name = StringField(label='partname')
    time_spend = StringField(label='timespendinmin')
    submit = SubmitField(label='submit')