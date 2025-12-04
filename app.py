"""
Main Flask application for Task Manager.
"""
from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime
import logging
from database import init_database, get_db
from models import SQLiteTaskRepository, Task

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Initialize repository
task_repo = SQLiteTaskRepository(get_db)


@app.route('/')
def index():
    """Home page - lists all tasks."""
    try:
        tasks = task_repo.get_all()
        return render_template('index.html', tasks=tasks, now=datetime.now)
    except Exception as e:
        logger.error(f"Error loading tasks: {e}")
        return render_template('index.html', tasks=[], error=str(e), now=datetime.now)


@app.route('/task/create', methods=['GET', 'POST'])
def create_task():
    """Create a new task."""
    if request.method == 'POST':
        try:
            # Get form data
            title = request.form.get('title', '').strip()
            description = request.form.get('description', '').strip()
            priority = int(request.form.get('priority', 3))
            due_date = request.form.get('due_date')
            due_date = due_date if due_date else None

            # Validate
            if not title:
                return render_template('edit_task.html',
                                       error="Title is required",
                                       title=title, description=description,
                                       priority=priority, due_date=due_date,
                                       now=datetime.now)

            # Create task
            task = Task(
                title=title,
                description=description,
                priority=priority,
                due_date=due_date
            )

            task_repo.create(task)
            logger.info(f"Created task: {title}")
            return redirect(url_for('index'))

        except Exception as e:
            logger.error(f"Error creating task: {e}")
            return render_template('edit_task.html',
                                   error=f"Error: {str(e)}",
                                   now=datetime.now,
                                   **request.form)

    # GET request - show empty form
    return render_template('edit_task.html', now=datetime.now)


@app.route('/task/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    """Edit an existing task."""
    task = task_repo.get_by_id(task_id)

    if not task:
        return redirect(url_for('index'))

    if request.method == 'POST':
        try:
            # Get form data
            update_data = {
                'title': request.form.get('title', '').strip(),
                'description': request.form.get('description', '').strip(),
                'priority': int(request.form.get('priority', 3)),
                'due_date': request.form.get('due_date')
            }

            # Validate
            if not update_data['title']:
                return render_template('edit_task.html',
                                       task=task,
                                       error="Title is required",
                                       now=datetime.now)

            # Update task
            updated_task = task_repo.update(task_id, update_data)

            if updated_task:
                logger.info(f"Updated task ID {task_id}")
                return redirect(url_for('index'))
            else:
                return render_template('edit_task.html',
                                       task=task,
                                       error="Failed to update task",
                                       now=datetime.now)

        except Exception as e:
            logger.error(f"Error updating task {task_id}: {e}")
            return render_template('edit_task.html',
                                   task=task,
                                   error=f"Error: {str(e)}",
                                   now=datetime.now)

    # GET request - show form with task data
    return render_template('edit_task.html', task=task, now=datetime.now)


@app.route('/task/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    """Delete a task."""
    try:
        success = task_repo.delete(task_id)
        if success:
            logger.info(f"Deleted task ID {task_id}")
            return jsonify({'success': True, 'message': 'Task deleted'})
        else:
            return jsonify({'success': False, 'message': 'Task not found'}), 404
    except Exception as e:
        logger.error(f"Error deleting task {task_id}: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/task/toggle/<int:task_id>', methods=['POST'])
def toggle_task(task_id):
    """Toggle task completion status."""
    try:
        task = task_repo.get_by_id(task_id)
        if not task:
            return jsonify({'success': False, 'message': 'Task not found'}), 404

        updated_task = task_repo.mark_completed(task_id, not task.completed)
        if updated_task:
            logger.info(
                f"Toggled task ID {task_id} to {updated_task.completed}")
            return jsonify({
                'success': True,
                'completed': updated_task.completed,
                'message': f'Task marked as {"completed" if updated_task.completed else "pending"}'
            })
        else:
            return jsonify({'success': False, 'message': 'Failed to update task'})
    except Exception as e:
        logger.error(f"Error toggling task {task_id}: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/tasks', methods=['GET'])
def api_get_tasks():
    """API endpoint to get all tasks."""
    try:
        tasks = task_repo.get_all()
        return jsonify([task.to_dict() for task in tasks])
    except Exception as e:
        logger.error(f"API error getting tasks: {e}")
        return jsonify({'error': str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return render_template('index.html',
                           error="Page not found",
                           tasks=task_repo.get_all(),
                           now=datetime.now), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors."""
    logger.error(f"Server error: {error}")
    return render_template('index.html',
                           error="Internal server error",
                           tasks=task_repo.get_all(),
                           now=datetime.now), 500


if __name__ == '__main__':
    # Initialize database
    init_database()

    # Run the application
    app.run(debug=True, host='0.0.0.0', port=5000)
