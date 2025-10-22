// PyTasker JavaScript Application
document.addEventListener('DOMContentLoaded', function() {
    // Initialize dark mode
    initializeTheme();
    
    // Add fade-in animation to main content
    document.querySelector('main').classList.add('fade-in');
    
    // Auto-hide alerts after 5 seconds
    setTimeout(() => {
        const alerts = document.querySelectorAll('.alert:not(.alert-info)');
        alerts.forEach(alert => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
});

/**
 * Theme Management
 */
function initializeTheme() {
    const themeToggle = document.getElementById('theme-toggle');
    const themeIcon = document.getElementById('theme-icon');
    const html = document.documentElement;
    
    if (!themeToggle || !themeIcon) return;
    
    // Get saved theme or default to light
    let currentTheme = localStorage.getItem('theme') || 'light';
    
    // Apply theme
    setTheme(currentTheme);
    
    // Theme toggle handler
    themeToggle.addEventListener('click', function() {
        currentTheme = currentTheme === 'light' ? 'dark' : 'light';
        setTheme(currentTheme);
    });
    
    function setTheme(theme) {
        html.setAttribute('data-bs-theme', theme);
        localStorage.setItem('theme', theme);
        
        // Update icon
        if (theme === 'dark') {
            themeIcon.className = 'bi bi-sun-fill';
            themeToggle.title = 'Switch to Light Mode';
        } else {
            themeIcon.className = 'bi bi-moon-fill';
            themeToggle.title = 'Switch to Dark Mode';
        }
        
        currentTheme = theme;
    }
}

/**
 * Task Management Functions
 */

// Quick status update
function updateTaskStatus(taskId, newStatus) {
    fetch(`/api/tasks/${taskId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ status: newStatus })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            showNotification('success', data.message);
            // Reload page to update UI
            setTimeout(() => location.reload(), 1000);
        }
    })
    .catch(error => {
        console.error('Error updating task:', error);
        showNotification('error', 'Failed to update task status');
    });
}

// Delete task with confirmation
function deleteTask(taskId, taskTitle) {
    if (confirm(`Are you sure you want to delete "${taskTitle}"?`)) {
        fetch(`/api/tasks/${taskId}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                showNotification('success', data.message);
                // Redirect to tasks list
                setTimeout(() => window.location.href = '/tasks', 1000);
            }
        })
        .catch(error => {
            console.error('Error deleting task:', error);
            showNotification('error', 'Failed to delete task');
        });
    }
}

/**
 * Utility Functions
 */

// Show notification
function showNotification(type, message) {
    const alertClass = type === 'error' ? 'danger' : type;
    const alertHTML = `
        <div class="alert alert-${alertClass} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    // Insert at the top of main content
    const main = document.querySelector('main');
    const container = main.querySelector('.container');
    if (container) {
        container.insertAdjacentHTML('afterbegin', alertHTML);
    }
}

// Form validation helpers
function validateTaskForm() {
    const title = document.getElementById('title');
    if (!title || !title.value.trim()) {
        showNotification('error', 'Task title is required');
        if (title) title.focus();
        return false;
    }
    
    if (title.value.length > 200) {
        showNotification('error', 'Task title must be 200 characters or less');
        title.focus();
        return false;
    }
    
    return true;
}

// Search and filter functionality
function initializeSearch() {
    const searchForm = document.querySelector('form[method="GET"]');
    if (!searchForm) return;
    
    // Auto-submit form on filter change (with debounce for search input)
    let searchTimeout;
    
    searchForm.addEventListener('change', function(e) {
        if (e.target.name === 'search') return; // Handle search separately
        
        // Auto-submit for select elements
        if (e.target.tagName === 'SELECT') {
            searchForm.submit();
        }
    });
    
    // Debounced search
    const searchInput = searchForm.querySelector('input[name="search"]');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                searchForm.submit();
            }, 500); // Wait 500ms after user stops typing
        });
    }
}

// Initialize search functionality
document.addEventListener('DOMContentLoaded', initializeSearch);

/**
 * API Helper Functions
 */

// Get task statistics
async function getTaskStats() {
    try {
        const response = await fetch('/api/stats');
        return await response.json();
    } catch (error) {
        console.error('Error fetching task stats:', error);
        return null;
    }
}

// Live update dashboard stats (if on dashboard)
function updateDashboardStats() {
    if (!window.location.pathname.includes('/')) return;
    
    getTaskStats().then(stats => {
        if (!stats) return;
        
        // Update stat cards if they exist
        const totalElement = document.querySelector('.stats-total');
        const todoElement = document.querySelector('.stats-todo');
        const progressElement = document.querySelector('.stats-progress');
        const doneElement = document.querySelector('.stats-done');
        
        if (totalElement) totalElement.textContent = stats.total_tasks;
        if (todoElement) todoElement.textContent = stats.todo_tasks;
        if (progressElement) progressElement.textContent = stats.in_progress_tasks;
        if (doneElement) doneElement.textContent = stats.done_tasks;
    });
}

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + N: New task (if authenticated)
    if ((e.ctrlKey || e.metaKey) && e.key === 'n') {
        const newTaskBtn = document.querySelector('a[href*="new_task"]');
        if (newTaskBtn) {
            e.preventDefault();
            newTaskBtn.click();
        }
    }
    
    // Ctrl/Cmd + /: Focus search
    if ((e.ctrlKey || e.metaKey) && e.key === '/') {
        const searchInput = document.querySelector('input[name="search"]');
        if (searchInput) {
            e.preventDefault();
            searchInput.focus();
        }
    }
    
    // Escape: Clear search/filters
    if (e.key === 'Escape') {
        const clearBtn = document.querySelector('a[href="/tasks"]');
        if (clearBtn && (document.activeElement.name === 'search' || 
                        document.activeElement.name === 'status' || 
                        document.activeElement.name === 'priority')) {
            clearBtn.click();
        }
    }
});

/**
 * Progressive Web App Features
 */

// Service Worker registration (for future PWA support)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        // Uncomment when service worker is implemented
        // navigator.serviceWorker.register('/sw.js');
    });
}

// Add to homescreen prompt handling
let deferredPrompt;
window.addEventListener('beforeinstallprompt', (e) => {
    deferredPrompt = e;
    // Show install button if desired
});

/**
 * Accessibility Improvements
 */

// Skip to main content
function addSkipLink() {
    const skipLink = document.createElement('a');
    skipLink.href = '#main-content';
    skipLink.textContent = 'Skip to main content';
    skipLink.className = 'visually-hidden-focusable btn btn-primary';
    skipLink.style.cssText = 'position: absolute; top: 10px; left: 10px; z-index: 9999;';
    
    document.body.insertBefore(skipLink, document.body.firstChild);
    
    const main = document.querySelector('main');
    if (main && !main.id) {
        main.id = 'main-content';
    }
}

document.addEventListener('DOMContentLoaded', addSkipLink);

// Announce dynamic content changes to screen readers
function announceToScreenReader(message) {
    const announcement = document.createElement('div');
    announcement.setAttribute('aria-live', 'polite');
    announcement.setAttribute('aria-atomic', 'true');
    announcement.className = 'visually-hidden';
    announcement.textContent = message;
    
    document.body.appendChild(announcement);
    
    setTimeout(() => {
        document.body.removeChild(announcement);
    }, 1000);
}

console.log('PyTasker JavaScript loaded successfully');