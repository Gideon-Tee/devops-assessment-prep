#!/usr/bin/env python3
"""
API-Based Log Upload Script
Reads local log files and uploads them to API endpoint with retry logic.
"""

import requests
import json
import time
import os
from pathlib import Path

# Configuration
API_ENDPOINT = "https://httpbin.org/post"  # Mock API for testing
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds
CHUNK_SIZE = 1024 * 1024  # 1MB chunks for large files

def read_log_file(file_path):
    """Read log file content"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"❌ Error reading {file_path}: {e}")
        return None

def upload_log_with_retry(file_path, content, api_endpoint=API_ENDPOINT):
    """Upload log content to API with retry logic"""
    payload = {
        'filename': os.path.basename(file_path),
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'size': len(content),
        'content': content
    }
    
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'LogUploader/1.0'
    }
    
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            print(f"📤 Uploading {file_path} (attempt {attempt}/{MAX_RETRIES})...")
            
            response = requests.post(
                api_endpoint,
                json=payload,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                print(f"✅ Successfully uploaded {file_path}")
                return True
            else:
                print(f"⚠️  Upload failed with status {response.status_code}: {response.text[:100]}")
                
        except requests.exceptions.Timeout:
            print(f"⏰ Upload timeout for {file_path} (attempt {attempt})")
        except requests.exceptions.ConnectionError:
            print(f"🔌 Connection error for {file_path} (attempt {attempt})")
        except requests.exceptions.RequestException as e:
            print(f"❌ Request error for {file_path}: {e}")
        
        if attempt < MAX_RETRIES:
            print(f"⏳ Retrying in {RETRY_DELAY} seconds...")
            time.sleep(RETRY_DELAY)
    
    print(f"❌ Failed to upload {file_path} after {MAX_RETRIES} attempts")
    return False

def upload_large_file_chunks(file_path, api_endpoint=API_ENDPOINT):
    """Upload large files in chunks"""
    file_size = os.path.getsize(file_path)
    
    if file_size <= CHUNK_SIZE:
        # Small file, upload normally
        content = read_log_file(file_path)
        if content is not None:
            return upload_log_with_retry(file_path, content, api_endpoint)
        return False
    
    # Large file, upload in chunks
    print(f"📦 Large file detected ({file_size} bytes), uploading in chunks...")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            chunk_num = 0
            while True:
                chunk = f.read(CHUNK_SIZE)
                if not chunk:
                    break
                
                chunk_num += 1
                chunk_filename = f"{os.path.basename(file_path)}.chunk{chunk_num}"
                
                success = upload_log_with_retry(chunk_filename, chunk, api_endpoint)
                if not success:
                    return False
        
        print(f"✅ Successfully uploaded {file_path} in {chunk_num} chunks")
        return True
        
    except Exception as e:
        print(f"❌ Error processing large file {file_path}: {e}")
        return False

def find_log_files(directory):
    """Find all log files in directory"""
    log_files = []
    for pattern in ['*.log', '*.txt']:
        log_files.extend(Path(directory).glob(pattern))
    return [str(f) for f in log_files if f.is_file()]

def create_sample_logs():
    """Create sample log files for testing"""
    os.makedirs("sample_logs", exist_ok=True)
    
    # Small log file
    with open("sample_logs/app.log", 'w') as f:
        f.write("2024-01-15 10:30:15 INFO Application started\n")
        f.write("2024-01-15 10:31:20 ERROR Database connection failed\n")
        f.write("2024-01-15 10:32:10 INFO Retrying connection\n")
    
    # Medium log file
    with open("sample_logs/access.log", 'w') as f:
        for i in range(100):
            f.write(f"2024-01-15 10:{30+i//10}:{i%60:02d} GET /api/users/{i} 200 {50+i}ms\n")
    
    print("📄 Sample log files created in sample_logs/")

def main():
    """Main function to upload log files"""
    print("🚀 Log Upload Script")
    
    # Get log directory
    log_dir = input("Enter log directory path (or press Enter for sample_logs): ").strip()
    if not log_dir:
        log_dir = "sample_logs"
        create_sample_logs()
    
    # Get API endpoint
    api_url = input(f"Enter API endpoint (or press Enter for {API_ENDPOINT}): ").strip()
    if not api_url:
        api_url = API_ENDPOINT
    
    # Find log files
    log_files = find_log_files(log_dir)
    
    if not log_files:
        print(f"❌ No log files found in {log_dir}")
        return
    
    print(f"📋 Found {len(log_files)} log files:")
    for log_file in log_files:
        print(f"  - {log_file}")
    
    # Upload each file
    successful_uploads = 0
    for log_file in log_files:
        if upload_large_file_chunks(log_file, api_url):
            successful_uploads += 1
    
    print(f"\n📊 Upload Summary:")
    print(f"  Successful: {successful_uploads}/{len(log_files)}")
    print(f"  Failed: {len(log_files) - successful_uploads}/{len(log_files)}")

if __name__ == "__main__":
    main()