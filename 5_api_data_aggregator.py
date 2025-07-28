#!/usr/bin/env python3
"""
REST API Data Aggregator
Fetches data from REST API, parses JSON, and displays aggregated statistics.
"""

import requests
import json
from collections import Counter

def fetch_api_data(url):
    """Fetch data from REST API endpoint"""
    try:
        print(f"🌐 Fetching data from: {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ API request failed: {e}")
        return None

def analyze_posts_data(posts):
    """Analyze posts data and generate statistics"""
    if not posts:
        return
    
    print(f"\n📊 POSTS ANALYSIS")
    print("=" * 40)
    print(f"Total posts: {len(posts)}")
    
    # User activity analysis
    user_posts = Counter(post['userId'] for post in posts)
    print(f"\n👥 Most active users:")
    for user_id, count in user_posts.most_common(5):
        print(f"  User {user_id}: {count} posts")
    
    # Title length analysis
    title_lengths = [len(post['title']) for post in posts]
    avg_title_length = sum(title_lengths) / len(title_lengths)
    print(f"\n📝 Title statistics:")
    print(f"  Average title length: {avg_title_length:.1f} characters")
    print(f"  Shortest title: {min(title_lengths)} characters")
    print(f"  Longest title: {max(title_lengths)} characters")
    
    # Body length analysis
    body_lengths = [len(post['body']) for post in posts]
    avg_body_length = sum(body_lengths) / len(body_lengths)
    print(f"\n📄 Body statistics:")
    print(f"  Average body length: {avg_body_length:.1f} characters")

def analyze_users_data(users):
    """Analyze users data and generate statistics"""
    if not users:
        return
    
    print(f"\n👤 USERS ANALYSIS")
    print("=" * 40)
    print(f"Total users: {len(users)}")
    
    # Domain analysis
    domains = [user['email'].split('@')[1] for user in users if '@' in user['email']]
    domain_counts = Counter(domains)
    print(f"\n📧 Email domains:")
    for domain, count in domain_counts.most_common():
        print(f"  {domain}: {count} users")
    
    # Company analysis
    companies = [user['company']['name'] for user in users if 'company' in user]
    company_counts = Counter(companies)
    print(f"\n🏢 Companies:")
    for company, count in company_counts.most_common(5):
        print(f"  {company}: {count} users")

def analyze_todos_data(todos):
    """Analyze todos data and generate statistics"""
    if not todos:
        return
    
    print(f"\n✅ TODOS ANALYSIS")
    print("=" * 40)
    print(f"Total todos: {len(todos)}")
    
    # Completion analysis
    completed = sum(1 for todo in todos if todo['completed'])
    completion_rate = (completed / len(todos)) * 100
    print(f"Completed: {completed} ({completion_rate:.1f}%)")
    print(f"Pending: {len(todos) - completed} ({100 - completion_rate:.1f}%)")
    
    # User productivity
    user_todos = {}
    for todo in todos:
        user_id = todo['userId']
        if user_id not in user_todos:
            user_todos[user_id] = {'total': 0, 'completed': 0}
        user_todos[user_id]['total'] += 1
        if todo['completed']:
            user_todos[user_id]['completed'] += 1
    
    print(f"\n📈 Top productive users:")
    sorted_users = sorted(user_todos.items(), 
                         key=lambda x: x[1]['completed'], reverse=True)
    for user_id, stats in sorted_users[:5]:
        completion_rate = (stats['completed'] / stats['total']) * 100
        print(f"  User {user_id}: {stats['completed']}/{stats['total']} ({completion_rate:.1f}%)")

def main():
    """Main function to demonstrate API data aggregation"""
    # Different API endpoints to test
    endpoints = {
        'posts': 'https://jsonplaceholder.typicode.com/posts',
        'users': 'https://jsonplaceholder.typicode.com/users',
        'todos': 'https://jsonplaceholder.typicode.com/todos'
    }
    
    print("🚀 REST API Data Aggregator")
    print("Available endpoints:")
    for key, url in endpoints.items():
        print(f"  {key}: {url}")
    
    choice = input("\nSelect endpoint (posts/users/todos) or press Enter for all: ").strip().lower()
    
    if choice and choice in endpoints:
        data = fetch_api_data(endpoints[choice])
        if data:
            if choice == 'posts':
                analyze_posts_data(data)
            elif choice == 'users':
                analyze_users_data(data)
            elif choice == 'todos':
                analyze_todos_data(data)
    else:
        # Analyze all endpoints
        for endpoint_name, url in endpoints.items():
            data = fetch_api_data(url)
            if data:
                if endpoint_name == 'posts':
                    analyze_posts_data(data)
                elif endpoint_name == 'users':
                    analyze_users_data(data)
                elif endpoint_name == 'todos':
                    analyze_todos_data(data)

if __name__ == "__main__":
    main()