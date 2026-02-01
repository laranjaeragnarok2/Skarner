
import socket
import psutil

PORT = 18789

print("--- DEBUGGING SKARNER MONITOR ---")

# 1. Check Port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(2)
try:
    result = s.connect_ex(('127.0.0.1', PORT))
    if result == 0:
        print(f"[SUCCESS] Connected to 127.0.0.1:{PORT}. Port is OPEN.")
    else:
        print(f"[FAIL] Could not connect to 127.0.0.1:{PORT}. Error code: {result}")
except Exception as e:
    print(f"[ERROR] Exception connecting: {e}")
s.close()

# 2. Check Process
print("\n--- CHECKING PROCESSES ---")
found = False
for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
    try:
        name = proc.info['name'].lower()
        if 'openclaw' in name or 'node' in name:
            print(f"Found suspect process: {name} (PID: {proc.info['pid']})")
            found = True
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        pass

if not found:
    print("No 'openclaw' or 'node' process found.")

print("\n--- DIAGNOSIS ---")
if result == 0:
    print("Monitor SHOULD be GREEN (Online).")
elif found:
    print("Monitor SHOULD be YELLOW (Process found, port closed).")
else:
    print("Monitor SHOULD be RED (Offline).")
