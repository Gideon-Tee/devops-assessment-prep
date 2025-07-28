#!/usr/bin/env python3
"""
API Status Checker with Alerting
Periodically checks API endpoints and sends alerts for failures or delays.
"""

import requests
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configuration
API_ENDPOINTS = [
    "https://httpbin.org/status/200",
    "https://httpbin.org/delay/1",
    "https://httpbin.org/status/500",
    "https://jsonplaceholder.typicode.com/posts/1"
]

TIMEOUT_THRESHOLD = 5  # seconds
CHECK_INTERVAL = 30    # seconds

def mock_send_alert(endpoint, status_code, response_time, error=None):
    """Mock alert function"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if error:
        print(f"🚨 [{timestamp}] ALERT: {endpoint} - ERROR: {error}")
    else:
        print(f"🚨 [{timestamp}] ALERT: {endpoint} - Status: {status_code}, Time: {response_time:.2f}s")

def check_endpoint(endpoint):
    """Check single API endpoint"""
    try:
        start_time = time.time()
        response = requests.get(endpoint, timeout=TIMEOUT_THRESHOLD)
        response_time = time.time() - start_time
        
        result = {
            'endpoint': endpoint,
            'status_code': response.status_code,
            'response_time': response_time,
            'success': 200 <= response.status_code < 300 and response_time <= TIMEOUT_THRESHOLD
        }
        
        # Log result
        status_icon = "✅" if result['success'] else "❌"
        print(f"{status_icon} {endpoint} - {response.status_code} ({response_time:.2f}s)")
        
        # Send alert if failed
        if not result['success']:
            if response_time > TIMEOUT_THRESHOLD:
                mock_send_alert(endpoint, response.status_code, response_time)
            elif not (200 <= response.status_code < 300):
                mock_send_alert(endpoint, response.status_code, response_time)
        
        return result
        
    except requests.exceptions.Timeout:
        print(f"⏰ {endpoint} - TIMEOUT")
        mock_send_alert(endpoint, None, TIMEOUT_THRESHOLD, "Request timeout")
        return {'endpoint': endpoint, 'success': False, 'error': 'timeout'}
        
    except requests.exceptions.RequestException as e:
        print(f"❌ {endpoint} - CONNECTION ERROR: {e}")
        mock_send_alert(endpoint, None, 0, str(e))
        return {'endpoint': endpoint, 'success': False, 'error': str(e)}

def check_all_endpoints():
    """Check all endpoints concurrently"""
    print(f"\n🔍 Checking {len(API_ENDPOINTS)} endpoints...")
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_endpoint = {executor.submit(check_endpoint, endpoint): endpoint 
                             for endpoint in API_ENDPOINTS}
        
        results = []
        for future in as_completed(future_to_endpoint):
            result = future.result()
            results.append(result)
    
    # Summary
    successful = sum(1 for r in results if r.get('success', False))
    print(f"📊 Summary: {successful}/{len(results)} endpoints healthy")
    
    return results

def monitor_apis():
    """Main monitoring loop"""
    print("🚀 Starting API Status Monitor...")
    print(f"📋 Monitoring endpoints: {len(API_ENDPOINTS)}")
    print(f"⏱️  Check interval: {CHECK_INTERVAL}s")
    print(f"⏰ Timeout threshold: {TIMEOUT_THRESHOLD}s")
    
    try:
        while True:
            check_all_endpoints()
            print(f"⏳ Waiting {CHECK_INTERVAL}s for next check...\n")
            time.sleep(CHECK_INTERVAL)
    except KeyboardInterrupt:
        print("\n🛑 Monitoring stopped")

if __name__ == "__main__":
    monitor_apis()