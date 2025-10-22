### 🧠 Prompt for GitHub Copilot Agent

> **Prompt:**
>
> Create a complete Python-based web application named **“PyTasker”**, a simple task management system similar to Jira, with the following requirements:
>
> 1. **Framework:** Use Flask (or FastAPI if more efficient).
> 2. **Database:** Use SQLite for local development with SQLAlchemy ORM.
> 3. **Features:**
>
>    * CRUD (Create, Read, Update, Delete) operations for tasks.
>    * Each task should have: Title, Description, Status (To Do, In Progress, Done), Priority, and Created/Updated timestamps.
>    * Optional user accounts (basic auth with username/password).
> 4. **Frontend/UI:**
>
>    * Use Bootstrap 5 or Tailwind CSS for a clean and responsive layout.
>    * Create pages for task list, add/edit task, and a simple dashboard showing task counts by status.
> 5. **API:** Include REST endpoints for tasks (JSON CRUD).
> 6. **Project structure:**
>
>    ```
>    /pytasker
>      ├── app.py
>      ├── models.py
>      ├── routes/
>      ├── static/
>      ├── templates/
>      ├── database.db
>      ├── requirements.txt
>      └── README.md
>    ```
> 7. **Setup GitHub Integration:**
>
>    * Initialize a new local git repo.
>    * Create a new public repo on GitHub named `pytasker`.
>    * Push all code and set up `.gitignore` for Python + Flask projects.
> 8. **Extras (optional):**
>
>    * Add search/filter for tasks by status or priority.
>    * Include dark mode toggle in the UI.
>    * Dockerfile for containerization.
>
> Finally, generate a clear `README.md` with setup steps and screenshots placeholders.

---

### 💡 Pro Tip:

If you want Copilot to iteratively refine the app:

* After the first generation, say:

  > “Add authentication and assign tasks to users.”
  > or
  > “Add Kanban-style task board using drag and drop.”
* Copilot Agent will update the code in context.

