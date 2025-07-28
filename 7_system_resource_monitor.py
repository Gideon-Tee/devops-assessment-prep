#!/usr/bin/env python3
"""
System Resource Monitor
Monitors CPU and memory usage, sends alerts when usage exceeds 80%.
"""

import psutil
import time
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

# Configuration
CPU_THRESHOLD = 80
MEMORY_THRESHOLD = 80
CHECK_INTERVAL = 10  # seconds

def mock_send_email(subject, message):
    """Mock email alert function"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"📧 [{timestamp}] ALERT EMAIL: {subject}")
    print(f"   Message: {message}")

def get_system_usage():
    """Get current CPU and memory usage"""
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    memory_percent = memory.percent
    
    return cpu_percent, memory_percent

def check_and_alert():
    """Check system usage and send alerts if thresholds exceeded"""
    cpu_usage, memory_usage = get_system_usage()
    
    print(f"💻 CPU: {cpu_usage:.1f}% | 🧠 Memory: {memory_usage:.1f}%")
    
    # Check CPU threshold
    if cpu_usage > CPU_THRESHOLD:
        subject = f"HIGH CPU USAGE ALERT - {cpu_usage:.1f}%"
        message = f"CPU usage has exceeded {CPU_THRESHOLD}% threshold. Current usage: {cpu_usage:.1f}%"
        mock_send_email(subject, message)
    
    # Check memory threshold
    if memory_usage > MEMORY_THRESHOLD:
        subject = f"HIGH MEMORY USAGE ALERT - {memory_usage:.1f}%"
        message = f"Memory usage has exceeded {MEMORY_THRESHOLD}% threshold. Current usage: {memory_usage:.1f}%"
        mock_send_email(subject, message)

def monitor_system():
    """Main monitoring loop"""
    print(f"🚀 System Resource Monitor Started")
    print(f"⚠️  CPU Threshold: {CPU_THRESHOLD}%")
    print(f"⚠️  Memory Threshold: {MEMORY_THRESHOLD}%")
    print(f"⏱️  Check Interval: {CHECK_INTERVAL}s")
    
    try:
        while True:
            check_and_alert()
            time.sleep(CHECK_INTERVAL)
    except KeyboardInterrupt:
        print("\n🛑 Monitoring stopped")

if __name__ == "__main__":
    monitor_system()