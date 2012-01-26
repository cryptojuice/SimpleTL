from flask import Flask, request, session, redirect, url_for,\
         abort, render_template, flash, Blueprint, escape
from task.models.users import *
from task.models.tasks import *
from redis import Redis

redis = Redis()

main = Blueprint('main', __name__)

t = Task()

#@main.route('/')
#def index():
#    return "Temp page"

@main.route('/')
def display_task():
    tasks = t.display_all(session['user_id'])
    return render_template("tasks.html", tasks=tasks)


@main.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if authenticate_user(request.form['email'], \
                request.form['password']):
            session['logged_in'] = True
            session['user_id'] = redis.hget("users:lookup:email", \
                    request.form['email'])
            return redirect(url_for('main.display_task'))
        else:
            session['logged_in'] = False
            flash('Incorrect login information')
            error = 'Incorrect login information'
    return render_template('login.html', error=error)

@main.route('/logout', methods=['GET', 'POST'])
def logout():
    error = None
    session['logged_in'] = False
    return redirect(url_for('main.login'))

@main.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        create_user(request.form['email'], request.form['password'])
        return redirect(url_for('main.login'))
    return render_template('signup.html', error=error)

@main.route('/new', methods=['GET', 'POST'])
def new_task():
    error=None
    if session['logged_in']:
        if request.method == 'POST':
            t.create_task(user_id=session['user_id'], note = request.form['note'])
            return redirect(url_for('main.display_task'))
    else:
        return redirect(url_for('main.login'))
    return render_template('tasks.html')

@main.route('/delete/<int:user_id>/<int:task_id>')
def delete_task(user_id, task_id):
    t.delete_task(user_id, task_id)
    return redirect(url_for('main.display_task'))

@main.route('/markcomplate/<int:user_id>/<int:task_id>')
def mark_complete(user_id, task_id):
    t.mark_complete(user_id, task_id)
    return redirect(url_for('main.display_task'))
