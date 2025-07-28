#!/usr/bin/env python3
"""
Real-Time Log Monitor
Continuously monitors a log file for ERROR entries and sends mock email alerts.
"""

import time
import re
import os

def mock_send_email(error_line):
    """Mock email alert function"""
    print(f"📧 ALERT EMAIL SENT: {error_line.strip()}")

def monitor_log(log_file_path="/var/log/app.log"):
    """Monitor log file for ERROR entries in real-time"""
    if not os.path.exists(log_file_path):
        print(f"Creating mock log file: {log_file_path}")
        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
        open(log_file_path, 'a').close()
    
    with open(log_file_path, 'r') as file:
        # Move to end of file
        file.seek(0, 2)
        
        print(f"🔍 Monitoring {log_file_path} for ERROR entries...")
        
        while True:
            line = file.readline()
            if line:
                # Case-insensitive ERROR detection
                if re.search(r'error', line, re.IGNORECASE):
                    print(f"❌ ERROR DETECTED: {line.strip()}")
                    mock_send_email(line)
            else:
                time.sleep(0.1)  # Brief pause when no new lines

if __name__ == "__main__":
    try:
        monitor_log()
    except KeyboardInterrupt:
        print("\n🛑 Monitoring stopped")
    except Exception as e:
        print(f"❌ Error: {e}")