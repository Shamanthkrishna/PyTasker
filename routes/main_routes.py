from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Task, User, TASK_STATUSES, TASK_PRIORITIES
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Dashboard with task statistics"""
    if current_user.is_authenticated:
        # Get user's tasks
        user_tasks = Task.query.filter_by(user_id=current_user.id).all()
        
        # Calculate statistics
        total_tasks = len(user_tasks)
        todo_tasks = len([t for t in user_tasks if t.status == 'To Do'])
        in_progress_tasks = len([t for t in user_tasks if t.status == 'In Progress'])
        done_tasks = len([t for t in user_tasks if t.status == 'Done'])
        
        # Recent tasks (last 5)
        recent_tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.updated_at.desc()).limit(5).all()
        
        return render_template('dashboard.html', 
                             total_tasks=total_tasks,
                             todo_tasks=todo_tasks,
                             in_progress_tasks=in_progress_tasks,
                             done_tasks=done_tasks,
                             recent_tasks=recent_tasks)
    else:
        # Public dashboard with all tasks
        all_tasks = Task.query.all()
        total_tasks = len(all_tasks)
        todo_tasks = len([t for t in all_tasks if t.status == 'To Do'])
        in_progress_tasks = len([t for t in all_tasks if t.status == 'In Progress'])
        done_tasks = len([t for t in all_tasks if t.status == 'Done'])
        
        return render_template('dashboard.html',
                             total_tasks=total_tasks,
                             todo_tasks=todo_tasks,
                             in_progress_tasks=in_progress_tasks,
                             done_tasks=done_tasks,
                             recent_tasks=[])

@main_bp.route('/tasks')
def tasks():
    """List all tasks with filtering options"""
    # Get filter parameters
    status_filter = request.args.get('status', '')
    priority_filter = request.args.get('priority', '')
    search_query = request.args.get('search', '')
    
    # Base query
    if current_user.is_authenticated:
        query = Task.query.filter_by(user_id=current_user.id)
    else:
        query = Task.query
    
    # Apply filters
    if status_filter and status_filter in TASK_STATUSES:
        query = query.filter(Task.status == status_filter)
    
    if priority_filter and priority_filter in TASK_PRIORITIES:
        query = query.filter(Task.priority == priority_filter)
    
    if search_query:
        query = query.filter(Task.title.contains(search_query) | Task.description.contains(search_query))
    
    # Order by updated date
    tasks = query.order_by(Task.updated_at.desc()).all()
    
    return render_template('tasks/list.html', 
                         tasks=tasks, 
                         statuses=TASK_STATUSES,
                         priorities=TASK_PRIORITIES,
                         current_status=status_filter,
                         current_priority=priority_filter,
                         current_search=search_query)

@main_bp.route('/tasks/new', methods=['GET', 'POST'])
@login_required
def new_task():
    """Create a new task"""
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description', '')
        status = request.form.get('status', 'To Do')
        priority = request.form.get('priority', 'Medium')
        
        if not title:
            flash('Title is required!', 'error')
            return render_template('tasks/form.html', 
                                 task=None, 
                                 statuses=TASK_STATUSES,
                                 priorities=TASK_PRIORITIES)
        
        task = Task(
            title=title,
            description=description,
            status=status,
            priority=priority,
            user_id=current_user.id
        )
        
        db.session.add(task)
        db.session.commit()
        
        flash('Task created successfully!', 'success')
        return redirect(url_for('main.tasks'))
    
    return render_template('tasks/form.html', 
                         task=None, 
                         statuses=TASK_STATUSES,
                         priorities=TASK_PRIORITIES)

@main_bp.route('/tasks/<int:task_id>')
def task_detail(task_id):
    """View task details"""
    task = Task.query.get_or_404(task_id)
    
    # Check if user can view this task
    if current_user.is_authenticated and task.user_id != current_user.id:
        flash('You can only view your own tasks!', 'error')
        return redirect(url_for('main.tasks'))
    
    return render_template('tasks/detail.html', task=task)

@main_bp.route('/tasks/<int:task_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    """Edit an existing task"""
    task = Task.query.get_or_404(task_id)
    
    # Check if user owns this task
    if task.user_id != current_user.id:
        flash('You can only edit your own tasks!', 'error')
        return redirect(url_for('main.tasks'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description', '')
        status = request.form.get('status')
        priority = request.form.get('priority')
        
        if not title:
            flash('Title is required!', 'error')
            return render_template('tasks/form.html', 
                                 task=task, 
                                 statuses=TASK_STATUSES,
                                 priorities=TASK_PRIORITIES)
        
        task.title = title
        task.description = description
        task.status = status
        task.priority = priority
        task.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        flash('Task updated successfully!', 'success')
        return redirect(url_for('main.task_detail', task_id=task.id))
    
    return render_template('tasks/form.html', 
                         task=task, 
                         statuses=TASK_STATUSES,
                         priorities=TASK_PRIORITIES)

@main_bp.route('/tasks/<int:task_id>/delete', methods=['POST'])
@login_required
def delete_task(task_id):
    """Delete a task"""
    task = Task.query.get_or_404(task_id)
    
    # Check if user owns this task
    if task.user_id != current_user.id:
        flash('You can only delete your own tasks!', 'error')
        return redirect(url_for('main.tasks'))
    
    db.session.delete(task)
    db.session.commit()
    
    flash('Task deleted successfully!', 'success')
    return redirect(url_for('main.tasks'))