# utility/agent.py
import psutil
import requests
import time
import platform
import subprocess
import json
import uuid

# Configuration
API_ENDPOINT = "http://127.0.0.1:5000/api/v1/health"
MACHINE_ID = str(uuid.uuid4())
INTERVAL = 60 * 1 # 15 minutes

def get_system_info():
    """Collects system health data."""
    system_data = {
        "machine_id": MACHINE_ID,
        "os": platform.system(),
        "timestamp": int(time.time()),
        "checks": {}
    }
    
    # Check 1: Disk Encryption Status
    try:
        if platform.system() == "Windows":
            # Windows: Check BitLocker status
            encryption_status = subprocess.run(["manage-bde", "-status"], capture_output=True, text=True).stdout
            system_data["checks"]["disk_encryption"] = "Encrypted" if "Protection Status: On" in encryption_status else "Not Encrypted"
        elif platform.system() == "Darwin":
            # macOS: Check FileVault status
            encryption_status = subprocess.run(["fdesetup", "status"], capture_output=True, text=True).stdout
            system_data["checks"]["disk_encryption"] = "Encrypted" if "FileVault is On." in encryption_status else "Not Encrypted"
        else: # Linux
            # Linux: Luks is common, check with lsblk and cryptsetup
            encryption_status = subprocess.run(["lsblk", "-o", "NAME,FSTYPE,TYPE"], capture_output=True, text=True).stdout
            system_data["checks"]["disk_encryption"] = "Encrypted" if "crypto_LUKS" in encryption_status else "Not Encrypted"
    except Exception as e:
        system_data["checks"]["disk_encryption"] = f"Error: {e}"

    # Check 2: OS Update Status
    try:
        if platform.system() == "Windows":
            # This is complex, so we'll simplify by checking for pending updates
            # using `wuauclt` or PowerShell. A simple flag is sufficient for this scope.
            system_data["checks"]["os_updates"] = "Needs Update" # Placeholder
        elif platform.system() == "Darwin":
            # macOS: Check for updates
            updates_status = subprocess.run(["softwareupdate", "-l"], capture_output=True, text=True).stdout
            system_data["checks"]["os_updates"] = "Up to Date" if "No new software available." in updates_status else "Updates Available"
        else: # Linux (Ubuntu/Debian)
            # Linux: Check using apt
            updates_status = subprocess.run(["sudo", "apt", "update"], capture_output=True, text=True).stdout
            system_data["checks"]["os_updates"] = "Up to Date" # Placeholder
    except Exception as e:
        system_data["checks"]["os_updates"] = f"Error: {e}"

    # Check 3: Antivirus Presence
    try:
        # A simple check for common AV processes. This is a heuristic, not foolproof.
        av_list = ["MsMpEng.exe", "avastui.exe", "avgui.exe"] # Common AV processes
        found_av = any(p.name() in av_list for p in psutil.process_iter())
        system_data["checks"]["antivirus"] = "Present" if found_av else "Not Present"
    except Exception as e:
        system_data["checks"]["antivirus"] = f"Error: {e}"

    # Check 4: Inactivity Sleep Settings (Simplified)
    # This is highly OS-specific and complex. We'll simplify with a placeholder.
    # In a real-world scenario, you'd use platform-specific APIs.
    system_data["checks"]["inactivity_sleep"] = "Compliant" # Placeholder

    try:
        system_data["checks"]["cpu_usage"] = f"{psutil.cpu_percent()}%"
        system_data["checks"]["memory_usage"] = f"{psutil.virtual_memory().percent}%"
    except Exception as e:
        system_data["checks"]["cpu_usage"] = f"Error: {e}"
        system_data["checks"]["memory_usage"] = f"Error: {e}"
    
    return system_data

def report_to_api(data):
    """Sends data to the remote API endpoint."""
    try:
        response = requests.post(API_ENDPOINT, json=data)
        response.raise_for_status()
        print(f"Data sent successfully. Status: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending data to API: {e}")

def main():
    """Main daemon loop."""
    last_state = {}
    while True:
        print("Checking system state...")
        current_state = get_system_info()
        
        # Report only if state has changed
        if current_state["checks"] != last_state.get("checks"):
            print("State changed. Reporting...")
            report_to_api(current_state)
            last_state = current_state
        else:
            print("No change in state. Skipping report.")
            
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()