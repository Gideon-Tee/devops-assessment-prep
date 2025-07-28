#!/usr/bin/env python3
"""
Cron Job Setup Script
Creates a cron job to run a script daily at midnight with logging.
"""

import os
import subprocess
from datetime import datetime

def create_sample_script():
    """Create a sample script to be scheduled"""
    script_content = '''#!/bin/bash
# Daily maintenance script
echo "$(date): Daily script executed" 
echo "System uptime: $(uptime)"
echo "Disk usage: $(df -h /)"
echo "Memory usage: $(free -h)"
echo "---"
'''
    
    script_path = "/usr/local/bin/daily_maintenance.sh"
    
    try:
        with open(script_path, 'w') as f:
            f.write(script_content)
        os.chmod(script_path, 0o755)
        print(f"✅ Created sample script: {script_path}")
        return script_path
    except PermissionError:
        # Fallback to local directory if no root access
        script_path = "./daily_maintenance.sh"
        with open(script_path, 'w') as f:
            f.write(script_content)
        os.chmod(script_path, 0o755)
        print(f"✅ Created sample script: {script_path}")
        return os.path.abspath(script_path)

def setup_cron_job(script_path, log_file="/var/log/daily_maintenance.log"):
    """Set up cron job to run script daily at midnight"""
    
    # Cron job entry: minute hour day month weekday command
    cron_entry = f"0 0 * * * {script_path} >> {log_file} 2>&1"
    
    try:
        # Get current crontab
        result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
        current_cron = result.stdout if result.returncode == 0 else ""
        
        # Check if job already exists
        if script_path in current_cron:
            print(f"⚠️  Cron job already exists for {script_path}")
            return
        
        # Add new cron job
        new_cron = current_cron + cron_entry + "\n"
        
        # Install new crontab
        process = subprocess.Popen(['crontab', '-'], stdin=subprocess.PIPE, text=True)
        process.communicate(input=new_cron)
        
        if process.returncode == 0:
            print(f"✅ Cron job created successfully")
            print(f"   Schedule: Daily at midnight (00:00)")
            print(f"   Script: {script_path}")
            print(f"   Log file: {log_file}")
        else:
            print(f"❌ Failed to create cron job")
            
    except FileNotFoundError:
        print("❌ crontab command not found. Install cron package.")
    except Exception as e:
        print(f"❌ Error setting up cron job: {e}")

def show_cron_jobs():
    """Display current cron jobs"""
    try:
        result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
        if result.returncode == 0 and result.stdout.strip():
            print("\n📋 Current cron jobs:")
            print(result.stdout)
        else:
            print("\n📋 No cron jobs found")
    except Exception as e:
        print(f"❌ Error listing cron jobs: {e}")

def main():
    """Main function to set up cron job"""
    print("🚀 Cron Job Setup Script")
    
    # Create sample script
    script_path = create_sample_script()
    
    # Set up log file path
    if os.geteuid() == 0:  # Running as root
        log_file = "/var/log/daily_maintenance.log"
    else:
        log_file = "./daily_maintenance.log"
        print("⚠️  Not running as root, using local log file")
    
    # Set up cron job
    setup_cron_job(script_path, log_file)
    
    # Show current cron jobs
    show_cron_jobs()
    
    print(f"\n📝 To manually test the script:")
    print(f"   {script_path}")
    print(f"\n📄 To view logs:")
    print(f"   tail -f {log_file}")

if __name__ == "__main__":
    main()