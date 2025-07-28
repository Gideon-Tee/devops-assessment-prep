#!/usr/bin/env python3
"""
Log Archive and Rotation
Finds old log files, compresses them, and moves to archive folder.
"""

import os
import gzip
import shutil
from datetime import datetime, timedelta
from pathlib import Path

def find_old_logs(log_directory, days_old=30):
    """Find log files older than specified days"""
    cutoff_date = datetime.now() - timedelta(days=days_old)
    old_logs = []
    
    for file_path in Path(log_directory).glob("*.log"):
        if file_path.is_file():
            file_mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
            if file_mtime < cutoff_date:
                old_logs.append(file_path)
    
    return old_logs

def compress_and_archive(log_file, archive_dir):
    """Compress log file and move to archive directory"""
    archive_path = Path(archive_dir)
    archive_path.mkdir(exist_ok=True)
    
    # Create compressed filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    compressed_name = f"{log_file.stem}_{timestamp}.gz"
    compressed_path = archive_path / compressed_name
    
    # Compress file
    with open(log_file, 'rb') as f_in:
        with gzip.open(compressed_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    
    print(f"📦 Archived: {log_file} → {compressed_path}")
    return compressed_path

def rotate_logs(log_directory="/var/log", archive_directory="./log_archive", days_old=30, delete_after_archive=True):
    """Main function to rotate and archive old logs"""
    print(f"🔍 Scanning {log_directory} for logs older than {days_old} days...")
    
    old_logs = find_old_logs(log_directory, days_old)
    
    if not old_logs:
        print("✅ No old logs found to archive")
        return
    
    print(f"📋 Found {len(old_logs)} old log files:")
    for log in old_logs:
        print(f"  - {log}")
    
    # Archive each old log
    archived_files = []
    for log_file in old_logs:
        try:
            archived_path = compress_and_archive(log_file, archive_directory)
            archived_files.append(archived_path)
            
            if delete_after_archive:
                os.remove(log_file)
                print(f"🗑️  Deleted original: {log_file}")
        except Exception as e:
            print(f"❌ Error processing {log_file}: {e}")
    
    print(f"\n✅ Archive complete! {len(archived_files)} files archived to {archive_directory}")

def create_sample_logs():
    """Create sample old log files for testing"""
    os.makedirs("sample_logs", exist_ok=True)
    
    # Create files with different ages
    for i in range(3):
        log_file = f"sample_logs/app_{i}.log"
        with open(log_file, 'w') as f:
            f.write(f"Sample log content {i}\n2024-01-{10+i} INFO: Application running\n")
        
        # Set file modification time to simulate old files
        old_time = (datetime.now() - timedelta(days=35+i)).timestamp()
        os.utime(log_file, (old_time, old_time))
    
    print("📄 Sample old log files created in sample_logs/")

if __name__ == "__main__":
    # For demo purposes, create sample logs
    create_sample_logs()
    
    # Run log rotation
    rotate_logs(
        log_directory="sample_logs",
        archive_directory="log_archive",
        days_old=30,
        delete_after_archive=True
    )