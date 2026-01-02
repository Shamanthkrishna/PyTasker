# 🚀 Setup TaskMate on a New Machine

This guide will help you run TaskMate on any Windows machine without needing to install MySQL or any database server.

## Quick Setup (5 minutes)

### 1. **Install Python** (if not already installed)
   - Download Python 3.8+ from [python.org](https://www.python.org/downloads/)
   - ✅ Make sure to check "Add Python to PATH" during installation

### 2. **Copy the TaskMate folder**
   - Simply copy the entire TaskMate folder to your new machine

### 3. **Open PowerShell/Command Prompt**
   - Navigate to the TaskMate folder:
     ```powershell
     cd C:\path\to\TaskMate
     ```

### 4. **Create Virtual Environment** (recommended)
   ```powershell
   python -m venv venv
   venv\Scripts\activate
   ```

### 5. **Install Dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

### 6. **Run the Application**
   ```powershell
   python app.py
   ```

### 7. **Open Browser**
   - Go to: `http://localhost:5000`
   - Login with:
     - **Username**: `admin`
     - **Password**: `admin123`

## ✅ That's It!

The application will automatically:
- Create a SQLite database (no MySQL needed!)
- Set up all tables
- Create a default admin user
- Add sample tasks

## 🔧 Troubleshooting

### Error: "python is not recognized"
- Python is not installed or not in PATH
- Reinstall Python and check "Add Python to PATH"

### Error: "No module named 'flask'"
- Dependencies not installed
- Run: `pip install -r requirements.txt`

### Port 5000 already in use
- Change port in app.py:
  ```python
  app.run(debug=True, host='0.0.0.0', port=5001)  # Use port 5001 instead
  ```

## 📝 Notes

- **Database**: The app uses SQLite by default (stored in `instance/taskmate.db`)
- **Portable**: You can copy the entire folder to any machine
- **No MySQL needed**: SQLite is built into Python
- **Fresh start**: Delete `instance/taskmate.db` to reset the database

## 🔄 Using MySQL (Optional)

If you prefer MySQL, set the DATABASE_URL environment variable:

```powershell
$env:DATABASE_URL="mysql+pymysql://username:password@localhost/database_name"
python app.py
```

But SQLite is recommended for portability!
