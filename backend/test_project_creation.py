"""Test script to create a project via API."""
import requests
import json
import time

# API endpoint
API_URL = "http://localhost:8000/api/projects"

# Create project request
project_data = {
    "prompt": "Build a simple calculator app with React",
    "name": "Calculator App Test",
    "description": "A test project for calculator"
}

print("Creating project...")
response = requests.post(API_URL, json=project_data)

if response.status_code == 200:
    project = response.json()
    project_id = project["id"]
    print(f"✅ Project created successfully!")
    print(f"   Project ID: {project_id}")
    print(f"   Status: {project['status']}")
    
    # Poll for completion
    print("\nWaiting for agent workflow to complete...")
    for i in range(30):  # Poll for 30 seconds
        time.sleep(2)
        status_response = requests.get(f"{API_URL}/{project_id}")
        if status_response.status_code == 200:
            project_status = status_response.json()
            print(f"   Status: {project_status['status']}")
            
            if project_status["status"] in ["completed", "failed"]:
                print(f"\n{'✅' if project_status['status'] == 'completed' else '❌'} Project {project_status['status']}!")
                if project_status.get("project_path"):
                    print(f"   Project path: {project_status['project_path']}")
                break
        else:
            print(f"   Error checking status: {status_response.status_code}")
else:
    print(f"❌ Failed to create project: {response.status_code}")
    print(response.text)
