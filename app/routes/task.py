from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app import db
from app.models import Task

task_bp = Blueprint('task', __name__)

# CRUD Operation


# Retrive/ Read:
@task_bp.route('/')
def view_task():
    if 'user' not in session:  #If user not logged in
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    task = Task.query.filter_by(user_id=user_id).all()
    return render_template('task.html', task = task, name = session['user'])


# Create :
@task_bp.route('/add', methods = ['POST'])
def add_task():
    if 'user' not in session:    #If user not logged in
        return redirect(url_for('auth.login'))

    title = request.form.get('title')
    user_id = session['user_id']

    if title:
        new_task = Task(title = title, user_id = user_id)
        db.session.add(new_task)
        db.session.commit()
        flash(f'Task {title} added successfully.', 'success')

    return redirect(url_for('task.view_task'))


# Update :
@task_bp.route('/toggle/<int:task_id>')
def update_status(task_id):    
    task = Task.query.get(task_id)
    if task:
        if task.status == 'pending':
            task.status = 'working'
        elif task.status == 'working':
            task.status = 'done'
        else:
            task.status = 'pending'
        db.session.commit()
    return redirect(url_for('task.view_task'))

# Delete :
@task_bp.route('/clear_all')
def clear_all():
    Task.query.delete()
    db.session.commit()
    flash('All tasks cleared!', 'info')
    return redirect(url_for('task.view_task'))

# Clear task :
@task_bp.route('/clear_task/<int:task_id>')
def clear_task(task_id):    
    task = Task.query.get(task_id)
    if task:
        flash(f'Task {task.title} removed successfully!', 'info')
        db.session.delete(task)
        db.session.commit()
    
    return redirect(url_for('task.view_task'))