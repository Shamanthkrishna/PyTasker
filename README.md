# 🧠 PyTasker

A modern, responsive task management web application built with Flask, similar to Jira but simplified for personal and team use.

![PyTasker Logo](https://via.placeholder.com/150x60/0d6efd/ffffff?text=PyTasker)

## ✨ Features

### 📋 Core Functionality
- **CRUD Operations**: Create, Read, Update, Delete tasks with ease
- **Task Management**: Title, Description, Status (To Do, In Progress, Done), Priority levels
- **User Authentication**: Secure login/register with session management
- **Dashboard**: Real-time statistics and task overview
- **Search & Filter**: Find tasks by status, priority, or search terms

### 🎨 User Interface
- **Responsive Design**: Bootstrap 5 powered, mobile-friendly interface
- **Dark Mode**: Toggle between light and dark themes
- **Intuitive Navigation**: Clean, modern interface with Bootstrap icons
- **Progress Visualization**: Visual progress bars and statistics

### 🚀 Technical Features
- **REST API**: JSON endpoints for all CRUD operations
- **SQLite Database**: Local development with SQLAlchemy ORM
- **Secure Authentication**: Password hashing with Werkzeug
- **Flash Messages**: User feedback system
- **Responsive Tables**: Mobile-optimized task listings

## 📸 Screenshots

> *Screenshots will be added here*

### Dashboard
![Dashboard Screenshot](https://via.placeholder.com/800x400/f8f9fa/6c757d?text=Dashboard+Screenshot)

### Task List
![Task List Screenshot](https://via.placeholder.com/800x400/f8f9fa/6c757d?text=Task+List+Screenshot)

### Task Detail
![Task Detail Screenshot](https://via.placeholder.com/800x400/f8f9fa/6c757d?text=Task+Detail+Screenshot)

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+ 
- Git

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/pytasker.git
   cd pytasker
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   
   # On Windows
   .venv\Scripts\activate
   
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   Visit `http://localhost:5000`

### Default Login
- **Username**: `admin`
- **Password**: `admin123`

## 📁 Project Structure

```
pytasker/
├── app.py                 # Main Flask application
├── models.py              # Database models (User, Task)
├── requirements.txt       # Python dependencies
├── database.db           # SQLite database (auto-created)
├── .gitignore            # Git ignore rules
├── routes/
│   ├── __init__.py       # Routes package
│   ├── main_routes.py    # Main application routes
│   ├── auth_routes.py    # Authentication routes
│   └── api_routes.py     # REST API endpoints
├── static/
│   ├── css/
│   │   └── style.css     # Custom styles
│   └── js/
│       └── app.js        # JavaScript functionality
├── templates/
│   ├── base.html         # Base template
│   ├── dashboard.html    # Dashboard page
│   ├── auth/
│   │   ├── login.html    # Login form
│   │   ├── register.html # Registration form
│   │   └── profile.html  # User profile
│   └── tasks/
│       ├── list.html     # Task list
│       ├── form.html     # Task create/edit
│       └── detail.html   # Task details
└── README.md             # This file
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the project root:

```env
SECRET_KEY=your-super-secret-key-here
FLASK_ENV=development
DATABASE_URL=sqlite:///database.db
```

### Database Setup
The database is automatically created on first run. To reset:

```bash
# Delete the database file
rm database.db

# Restart the application
python app.py
```

## 🌐 API Endpoints

### Authentication Required Routes
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Dashboard |
| GET | `/tasks` | List tasks |
| GET | `/tasks/new` | New task form |
| POST | `/tasks/new` | Create task |
| GET | `/tasks/<id>` | Task details |
| GET | `/tasks/<id>/edit` | Edit task form |
| POST | `/tasks/<id>/edit` | Update task |
| POST | `/tasks/<id>/delete` | Delete task |

### REST API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/tasks` | Get all tasks (JSON) |
| POST | `/api/tasks` | Create task (JSON) |
| GET | `/api/tasks/<id>` | Get task (JSON) |
| PUT | `/api/tasks/<id>` | Update task (JSON) |
| DELETE | `/api/tasks/<id>` | Delete task (JSON) |
| GET | `/api/stats` | Get statistics (JSON) |

### Example API Usage

```javascript
// Get all tasks
fetch('/api/tasks')
  .then(response => response.json())
  .then(data => console.log(data));

// Create a new task
fetch('/api/tasks', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    title: 'New Task',
    description: 'Task description',
    status: 'To Do',
    priority: 'Medium'
  })
});
```

## 🚀 Deployment

### Using Docker (Optional)

1. **Create Dockerfile**
   ```dockerfile
   FROM python:3.11-slim

   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt

   COPY . .
   EXPOSE 5000

   CMD ["python", "app.py"]
   ```

2. **Build and run**
   ```bash
   docker build -t pytasker .
   docker run -p 5000:5000 pytasker
   ```

### Production Deployment

For production, consider:
- Use PostgreSQL or MySQL instead of SQLite
- Set proper environment variables
- Use a WSGI server like Gunicorn
- Configure reverse proxy (Nginx)
- Enable HTTPS

## 🧪 Testing

Run the application in development mode:

```bash
export FLASK_ENV=development
python app.py
```

### Manual Testing Checklist
- [ ] User registration and login
- [ ] Task creation, editing, deletion
- [ ] Search and filtering
- [ ] Dark mode toggle
- [ ] Mobile responsiveness
- [ ] API endpoints

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📋 TODO & Future Enhancements

- [ ] Email notifications
- [ ] Task comments/notes
- [ ] File attachments
- [ ] Task templates
- [ ] Team collaboration features
- [ ] Calendar integration
- [ ] Mobile app (React Native/Flutter)
- [ ] Kanban board view
- [ ] Task dependencies
- [ ] Time tracking
- [ ] Reporting and analytics

## 🐛 Known Issues

- None currently reported

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Your Name** - *Initial work* - [YourGitHub](https://github.com/yourusername)

## 🙏 Acknowledgments

- [Flask](https://flask.palletsprojects.com/) - Web framework
- [Bootstrap](https://getbootstrap.com/) - CSS framework
- [Bootstrap Icons](https://icons.getbootstrap.com/) - Icon library
- [SQLAlchemy](https://www.sqlalchemy.org/) - Database ORM

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/pytasker/issues) page
2. Create a new issue if needed
3. Contact: your.email@example.com

---

**PyTasker** - Making task management simple and efficient! 🎯