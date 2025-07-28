# DevOps Assessment Solutions

This repository contains solutions for 6 common DevOps coding interview questions.

## Solutions Overview

### 1. Real-Time Log Monitor (`1_realtime_log_monitor.py`)
**Problem**: Monitor log file for ERROR entries in real-time
- Watches file continuously (tail-like behavior)
- Case-insensitive ERROR detection
- Mock email alerts

**Usage**:
```bash
python3 1_realtime_log_monitor.py
# Creates /var/log/app.log if it doesn't exist
# Add test entries: echo "2024-01-15 ERROR: Test error" >> /var/log/app.log
```

### 2. Log Parsing and Sorting (`2_log_parser_sorter.py`)
**Problem**: Parse logs, filter errors, group by type, generate frequency report
- Extracts timestamps and error types
- Groups errors by type
- Shows most frequent errors

**Usage**:
```bash
python3 2_log_parser_sorter.py
# Creates sample.log automatically or specify your own log file
```

### 3. Archive and Rotate Old Logs (`3_log_archiver.py`)
**Problem**: Archive old logs to compressed format
- Finds logs older than specified days
- Compresses to .gz format
- Moves to archive directory

**Usage**:
```bash
python3 3_log_archiver.py
# Creates sample old logs and demonstrates archiving
```

### 4. API Status Checker (`4_api_status_checker.py`)
**Problem**: Monitor API endpoints and send alerts
- Concurrent endpoint checking
- Timeout and status code monitoring
- Mock alert system

**Usage**:
```bash
python3 4_api_status_checker.py
# Monitors predefined endpoints every 30 seconds
# Press Ctrl+C to stop
```

### 5. REST API Data Aggregator (`5_api_data_aggregator.py`)
**Problem**: Fetch API data and generate statistics
- Fetches from JSONPlaceholder API
- Analyzes posts, users, and todos
- Generates statistical summaries

**Usage**:
```bash
python3 5_api_data_aggregator.py
# Choose specific endpoint or analyze all
```

### 6. API-Based Log Upload (`6_log_uploader.py`)
**Problem**: Upload log files to API endpoint with retry logic
- Handles large files with chunking
- Retry mechanism with exponential backoff
- Error handling and reporting

**Usage**:
```bash
python3 6_log_uploader.py
# Creates sample logs or specify directory
# Uses httpbin.org for testing
```

## Requirements

Install required packages:
```bash
pip3 install requests
```

## Key Features Demonstrated

- **File I/O**: Reading, writing, monitoring files
- **API Integration**: HTTP requests, JSON parsing
- **Error Handling**: Try-catch blocks, retry logic
- **Concurrency**: Threading for parallel operations
- **Data Processing**: Parsing, filtering, aggregation
- **System Operations**: File compression, archiving
- **Real-time Monitoring**: Continuous file watching
- **Logging**: Structured output and alerts

## Testing Tips

1. **Log Monitor**: Use `tail -f` in another terminal to add test entries
2. **API Checker**: Modify endpoints list to test different scenarios
3. **Log Parser**: Create custom log files with different error patterns
4. **Archiver**: Adjust `days_old` parameter for testing
5. **Data Aggregator**: Try different API endpoints
6. **Log Uploader**: Test with various file sizes

Each script includes comprehensive error handling and can be easily modified for specific requirements.