from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from models import db, Task, User, TASK_STATUSES, TASK_PRIORITIES
from datetime import datetime

api_bp = Blueprint('api', __name__)

@api_bp.route('/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks (JSON API)"""
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
    
    # Get tasks
    tasks = query.order_by(Task.updated_at.desc()).all()
    
    return jsonify({
        'tasks': [task.to_dict() for task in tasks],
        'total': len(tasks)
    })

@api_bp.route('/tasks', methods=['POST'])
@login_required
def create_task():
    """Create a new task (JSON API)"""
    data = request.get_json()
    
    if not data or not data.get('title'):
        return jsonify({'error': 'Title is required'}), 400
    
    # Validate status and priority
    status = data.get('status', 'To Do')
    priority = data.get('priority', 'Medium')
    
    if status not in TASK_STATUSES:
        return jsonify({'error': 'Invalid status'}), 400
    
    if priority not in TASK_PRIORITIES:
        return jsonify({'error': 'Invalid priority'}), 400
    
    task = Task(
        title=data['title'],
        description=data.get('description', ''),
        status=status,
        priority=priority,
        user_id=current_user.id
    )
    
    db.session.add(task)
    db.session.commit()
    
    return jsonify({
        'message': 'Task created successfully',
        'task': task.to_dict()
    }), 201

@api_bp.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Get a specific task (JSON API)"""
    task = Task.query.get_or_404(task_id)
    
    # Check if user can view this task
    if current_user.is_authenticated and task.user_id != current_user.id:
        return jsonify({'error': 'Access denied'}), 403
    
    return jsonify({'task': task.to_dict()})

@api_bp.route('/tasks/<int:task_id>', methods=['PUT'])
@login_required
def update_task(task_id):
    """Update a task (JSON API)"""
    task = Task.query.get_or_404(task_id)
    
    # Check if user owns this task
    if task.user_id != current_user.id:
        return jsonify({'error': 'Access denied'}), 403
    
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Update fields
    if 'title' in data:
        if not data['title']:
            return jsonify({'error': 'Title cannot be empty'}), 400
        task.title = data['title']
    
    if 'description' in data:
        task.description = data['description']
    
    if 'status' in data:
        if data['status'] not in TASK_STATUSES:
            return jsonify({'error': 'Invalid status'}), 400
        task.status = data['status']
    
    if 'priority' in data:
        if data['priority'] not in TASK_PRIORITIES:
            return jsonify({'error': 'Invalid priority'}), 400
        task.priority = data['priority']
    
    task.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({
        'message': 'Task updated successfully',
        'task': task.to_dict()
    })

@api_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
@login_required
def delete_task(task_id):
    """Delete a task (JSON API)"""
    task = Task.query.get_or_404(task_id)
    
    # Check if user owns this task
    if task.user_id != current_user.id:
        return jsonify({'error': 'Access denied'}), 403
    
    db.session.delete(task)
    db.session.commit()
    
    return jsonify({'message': 'Task deleted successfully'})

@api_bp.route('/stats', methods=['GET'])
def get_stats():
    """Get task statistics (JSON API)"""
    if current_user.is_authenticated:
        # User-specific stats
        user_tasks = Task.query.filter_by(user_id=current_user.id).all()
        
        stats = {
            'total_tasks': len(user_tasks),
            'todo_tasks': len([t for t in user_tasks if t.status == 'To Do']),
            'in_progress_tasks': len([t for t in user_tasks if t.status == 'In Progress']),
            'done_tasks': len([t for t in user_tasks if t.status == 'Done']),
            'priority_breakdown': {
                'low': len([t for t in user_tasks if t.priority == 'Low']),
                'medium': len([t for t in user_tasks if t.priority == 'Medium']),
                'high': len([t for t in user_tasks if t.priority == 'High']),
                'critical': len([t for t in user_tasks if t.priority == 'Critical'])
            }
        }
    else:
        # Public stats
        all_tasks = Task.query.all()
        
        stats = {
            'total_tasks': len(all_tasks),
            'todo_tasks': len([t for t in all_tasks if t.status == 'To Do']),
            'in_progress_tasks': len([t for t in all_tasks if t.status == 'In Progress']),
            'done_tasks': len([t for t in all_tasks if t.status == 'Done']),
            'priority_breakdown': {
                'low': len([t for t in all_tasks if t.priority == 'Low']),
                'medium': len([t for t in all_tasks if t.priority == 'Medium']),
                'high': len([t for t in all_tasks if t.priority == 'High']),
                'critical': len([t for t in all_tasks if t.priority == 'Critical'])
            }
        }
    
    return jsonify(stats)