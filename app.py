from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
import os
from datetime import datetime

from models import db, User, Task, TASK_STATUSES, TASK_PRIORITIES

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    db.init_app(app)
    
    # Login manager setup
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Register blueprints
    from routes.main_routes import main_bp
    from routes.auth_routes import auth_bp
    from routes.api_routes import api_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Create database tables
    with app.app_context():
        db.create_all()
        
        # Create default admin user if no users exist
        if not User.query.first():
            admin_user = User(
                username='admin',
                email='admin@taskmate.com'
            )
            admin_user.set_password('admin123')
            db.session.add(admin_user)
            
            # Create sample tasks
            sample_tasks = [
                Task(
                    title='Setup TaskMate Project',
                    description='Initialize the TaskMate task management application with Flask and SQLAlchemy',
                    status='Done',
                    priority='High',
                    user_id=1
                ),
                Task(
                    title='Create User Authentication',
                    description='Implement user registration, login, and session management',
                    status='In Progress',
                    priority='Medium',
                    user_id=1
                ),
                Task(
                    title='Build Dashboard',
                    description='Create a dashboard showing task statistics and overview',
                    status='To Do',
                    priority='Medium',
                    user_id=1
                )
            ]
            
            for task in sample_tasks:
                db.session.add(task)
            
            db.session.commit()
            print("Default admin user created: admin/admin123")
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)