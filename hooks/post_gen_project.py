#!/usr/bin/env python
import os
import shutil
import subprocess

# Get variables from cookiecutter
use_analytics = '{{ cookiecutter.use_analytics }}' == 'yes'
use_authentication = '{{ cookiecutter.use_authentication }}' == 'yes'
use_comments = '{{ cookiecutter.use_comments }}' == 'yes'
auto_commit_enabled = '{{ cookiecutter.auto_commit_enabled }}' == 'yes'
file_watcher_enabled = '{{ cookiecutter.file_watcher_enabled }}' == 'yes'

print("Configuring your knowledge base project...")

# Remove unnecessary integration files
if not use_analytics:
    analytics_file = os.path.join('scripts', 'analytics_integration.py')
    if os.path.exists(analytics_file):
        os.remove(analytics_file)
        print(f"Removed {analytics_file}")

if not use_authentication:
    auth_file = os.path.join('scripts', 'auth_integration.py')
    if os.path.exists(auth_file):
        os.remove(auth_file)
        print(f"Removed {auth_file}")

if not use_comments:
    comments_file = os.path.join('scripts', 'comments_integration.py')
    if os.path.exists(comments_file):
        os.remove(comments_file)
        print(f"Removed {comments_file}")

if not auto_commit_enabled:
    autocommit_file = os.path.join('scripts', 'auto_commit.py')
    if os.path.exists(autocommit_file):
        os.remove(autocommit_file)
        print(f"Removed {autocommit_file}")
    
    log_file = 'auto_commit.log'
    if os.path.exists(log_file):
        os.remove(log_file)
        print(f"Removed {log_file}")

if not file_watcher_enabled:
    watcher_file = os.path.join('scripts', 'watch_changes.py')
    if os.path.exists(watcher_file):
        os.remove(watcher_file)
        print(f"Removed {watcher_file}")
    
    log_file = 'file_watcher.log'
    if os.path.exists(log_file):
        os.remove(log_file)
        print(f"Removed {log_file}")

# Set up license based on choice
license_choice = '{{ cookiecutter.open_source_license }}'
if license_choice == "Not open source":
    if os.path.exists('LICENSE'):
        os.remove('LICENSE')
        print("Removed LICENSE file as project is not open source")

# Initialize git repository
try:
    print("Initializing git repository...")
    subprocess.run(['git', 'init'], check=True)
    subprocess.run(['git', 'add', '.'], check=True)
    subprocess.run(['git', 'commit', '-m', 'Initial commit from cookiecutter template'], check=True)
    print("Git repository initialized with initial commit")
except subprocess.CalledProcessError as e:
    print(f"Warning: Git initialization failed: {e}")
except FileNotFoundError:
    print("Warning: Git not found. Please initialize the repository manually.")

print(f"\nProject '{{ cookiecutter.project_name }}' created successfully!")
print("To get started, run:")
print("  cd {{ cookiecutter.project_slug }}")
print("  pip install -r requirements.txt")
print("  mkdocs serve")
