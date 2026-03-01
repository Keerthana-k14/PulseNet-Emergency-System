import subprocess
import sys
import os
import time
import threading

agents = [
    {"name": "COORDINATOR", "cwd": "coordinator_home", "path": "coordination_agent.py"},
    {"name": "MEDICAL    ", "cwd": "medical_home", "path": "medical_agent.py"},
    {"name": "AMBULANCE  ", "cwd": "ambulance_home", "path": "ambulance_agent.py"},
    {"name": "TRAFFIC    ", "cwd": "traffic_home", "path": "traffic_agent.py"},
    {"name": "HOSPITAL   ", "cwd": "hospital_home", "path": "hospital_agent.py"},
    {"name": "DOCTOR     ", "cwd": "doctor_home", "path": "doctor_agent.py"},
]

processes = []
log_lock = threading.Lock()

# Initialize clean log file
with open("ui_logs.txt", "w", encoding="utf-8") as f:
    f.write("System Initialized. Awaiting incident reports...\n")

def read_output(process, name):
    for line in iter(process.stdout.readline, ''):
        if line:
            clean_line = line.strip()
            print(f"[{name}] {clean_line}")
            
            # Filter out Werkzeug web server noise for the Streamlit UI
            if "werkzeug" not in clean_line.lower() and "http" not in clean_line.lower() and "address" not in clean_line.lower():
                with log_lock:
                    with open("ui_logs.txt", "a", encoding="utf-8") as log_file:
                        log_file.write(f"[{name}] {clean_line}\n")
                        log_file.flush()

print("--- STARTING PULSENET AI SWARM ---")
python_exe = sys.executable

try:
    for a in agents:
        print(f"Started {a['name'].strip()}...")
        p = subprocess.Popen(
            [python_exe, "-u", a['path']],
            cwd=os.path.abspath(a['cwd']),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        processes.append(p)
        t = threading.Thread(target=read_output, args=(p, a['name']), daemon=True)
        t.start()
        time.sleep(4) # Prevent rate-limiting

    print("\n--- ALL AGENTS LIVE ---")
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("\nShutting down ecosystem...")
    for p in processes:
        p.terminate()
    sys.exit(0)