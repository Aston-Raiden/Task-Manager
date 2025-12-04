Task Manager Web Application
A full-featured task management web application built with Python Flask, HTML, CSS, and SQLite database.

Features
✅ Create tasks with title, description, priority, and due date
✅ Update existing tasks
✅ Delete tasks
✅ List all tasks with sorting (priority, due date, completion status)
✅ Mark tasks as completed/pending
✅ Responsive design for mobile and desktop
✅ RESTful API endpoints
✅ Comprehensive unit tests
Tech Stack
Backend: Python 3.8+ with Flask
Frontend: HTML5, CSS3, Vanilla JavaScript
Database: SQLite with SQLAlchemy-like ORM pattern
Testing: Python unittest framework
Prerequisites
Python 3.8 or higher
pip (Python package manager)
Installation
STEP 1: Download the Project Method A: Download ZIP (Easiest)

Go to your GitHub repository: https://github.com/Aston-Raiden/Task-Manager Click the green "Code" button Select "Download ZIP"

Extract the ZIP file to a folder on your computer (e.g., Desktop/task-manager), when extracting make sure you store the main unzipped folder titled Task-Manager-main, in the main directory of either the downloads or desktop.

command prompt should look like this:
C:\Users\"Your username"\Downloads\Task-Manager-main
or
C:\Users\"Your username"\Desktop\Task-Manager-main

STEP 2: Install Python (If Not Installed) Check if Python is installed:

python --version

Should show: Python 3.x.x
If not installed, download from:

Windows: python.org/downloads Mac: Comes pre-installed or use Homebrew: brew install python Linux: sudo apt install python3 python3-pip

During installation (Windows):

✅ Check "Add Python to PATH"

Click "Install Now"

STEP 3: Install Flask Open Command Prompt/Terminal in project folder:

Navigate to project folder

cd C:\Users\"Your username"\Downloads\Task-Manager-main
or
C:\Users\"Your username"\Desktop\Task-Manager-main

Install Flask
pip install -r requirements.txt pip install Flask==2.3.3

If pip doesn't work, try:
python -m pip install Flask==2.3.3

Or on Mac/Linux:
pip3 install Flask==2.3.3

Verify installation: pip list | grep Flask

Should show: Flask 2.3.3
STEP 4: Run the Application

Make sure you're in the project folder
cd task-manager

Run the app
python app.py

If that doesn't work, try:
python3 app.py

or
py app.py You should see:

text

Serving Flask app 'app'
Debug mode: on
Running on http://127.0.0.1:5000 Press CTRL+C to quit STEP 5: Open in Browser Open your web browser (Chrome, Firefox, Edge, Safari)
Go to: http://localhost:5000

OR click the link in the terminal: http://127.0.0.1:5000

Before or after testing the web application, you can run python test_app.py in the terminal to see if passes all the created unit tests

STEP 6: Test the Application Test all features: Create a task: Click "Add New Task" button Edit a task: Click pencil icon on any task Delete a task: Click trash icon on any task Mark as complete: Click checkmark icon View API: Click "View API" button or go to http://localhost:5000/api/tasks
