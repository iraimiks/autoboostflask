from rapackege import app,db
import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash
from rapackege.models import Users

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        app.logger.info('testing info log')
        if not username:
            error = 'Username is required'
        elif not password:
            error = 'Passowrd is required'
        if error is None:
            try:
                new_user = Users(
                    user_role = "user_worker",
                    username = username,
                    password = password
                )
                db.session.add(new_user)
                db.session.commit()
            except ValueError:
                error = f"User {username} is allredy registerd."
            else:
                return redirect(url_for("auth.register"))
        flash(error)
    return render_template("auth/register.html")

@bp.route('/login', methods=('GET','POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Users.query.filter_by(username=username).first()
        error = None
        if user is None:
            error = 'Incorrect username'
        elif not check_password_hash(user.password,password):
            error = 'Incorrect password'
        if error is None:
            session.clear()
            session['user_id'] = user.id
            # hear will be if else statment wher if admin_satus go to /dashbord
            return redirect(url_for('worker_cars',id=user.id))
        flash(error)
    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = Users.query.filter_by(id=user_id).first()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

#def admin_required(view):
#    @functools.wraps(view)
#    def wrapped_view(**kwargs):
#        app.logger.info('Check:', g.user, 'Check role:',g.user.user_role)
#        if g.user.user_role != "Admin":
#            return redirect(url_for('auth.login'))
#        else:
#            app.logger.info('testing inssfo log')
#        return view(**kwargs)
#    return wrapped_view