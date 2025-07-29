import subprocess
import sys
import os

# Ensure we are in the root directory (mongo-task2)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(BASE_DIR)

# Add the project root to sys.path so 'app' is importable
sys.path.insert(0, BASE_DIR)

services = [
    ("app.router.auth.authentication:app", 8005),
    ("app.router.Attendance.atten:app", 8006),
    ("app.router.Salary.paisa:app", 8007),
    ("app.router.Holidays.holiday:app", 8008),
    ("app.router.User.promote:app", 8009),
]

processes = []

for module, port in services:
    print(f"Starting {module} on port {port}")
    p = subprocess.Popen([
        sys.executable, "-m", "uvicorn", module,
        "--host", "0.0.0.0",
        "--port", str(port),
        "--reload"
    ])
    processes.append(p)

try:
    for p in processes:
        p.wait()
except KeyboardInterrupt:
    print("Stopping all services...")
    for p in processes:
        p.terminate()
