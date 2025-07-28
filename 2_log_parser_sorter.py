#!/usr/bin/env python3
"""
Log Parsing and Sorting
Reads log file, filters ERROR entries, groups by error type, and generates frequency report.
"""

import re
from collections import Counter
from datetime import datetime

def parse_log_file(log_file_path):
    """Parse log file and extract ERROR entries with timestamps"""
    errors = []
    
    try:
        with open(log_file_path, 'r') as file:
            for line in file:
                if re.search(r'error', line, re.IGNORECASE):
                    # Extract timestamp and error type
                    timestamp_match = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', line)
                    error_type_match = re.search(r'ERROR:?\s*(\w+)', line, re.IGNORECASE)
                    
                    timestamp = timestamp_match.group() if timestamp_match else "Unknown"
                    error_type = error_type_match.group(1) if error_type_match else "Generic"
                    
                    errors.append({
                        'timestamp': timestamp,
                        'error_type': error_type,
                        'full_line': line.strip()
                    })
    except FileNotFoundError:
        print(f"❌ Log file not found: {log_file_path}")
        return []
    
    return errors

def generate_error_report(errors):
    """Generate sorted report of most frequent errors"""
    if not errors:
        print("No errors found in log file")
        return
    
    # Count error types
    error_counts = Counter(error['error_type'] for error in errors)
    
    print("📊 ERROR FREQUENCY REPORT")
    print("=" * 40)
    print(f"Total errors found: {len(errors)}")
    print("\nMost frequent errors:")
    
    for error_type, count in error_counts.most_common():
        print(f"  {error_type}: {count} occurrences")
    
    print("\n📝 Recent error samples:")
    for error in errors[-3:]:  # Show last 3 errors
        print(f"  [{error['timestamp']}] {error['error_type']}: {error['full_line'][:80]}...")

def create_sample_log():
    """Create sample log file for testing"""
    sample_log = """2024-01-15 10:30:15 INFO Application started
2024-01-15 10:31:20 ERROR ConnectionError Failed to connect to database
2024-01-15 10:32:10 INFO Processing request
2024-01-15 10:33:45 ERROR ValidationError Invalid user input
2024-01-15 10:34:12 ERROR ConnectionError Database timeout
2024-01-15 10:35:30 INFO Request completed
2024-01-15 10:36:15 ERROR AuthenticationError Invalid credentials
2024-01-15 10:37:22 ERROR ValidationError Missing required field
2024-01-15 10:38:10 ERROR ConnectionError Network unreachable"""
    
    with open('sample.log', 'w') as f:
        f.write(sample_log)
    print("📄 Sample log file created: sample.log")

if __name__ == "__main__":
    log_file = input("Enter log file path (or press Enter for sample.log): ").strip()
    
    if not log_file:
        log_file = "sample.log"
        create_sample_log()
    
    errors = parse_log_file(log_file)
    generate_error_report(errors)