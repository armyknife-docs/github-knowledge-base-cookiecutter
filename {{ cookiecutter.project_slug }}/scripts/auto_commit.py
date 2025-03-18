#!/usr/bin/env python3
"""
Auto-commit script that monitors changes in the docs directory and 
automatically commits and pushes them to the GitHub repository.
"""

import os
import sys
import subprocess
import time
import logging
from datetime import datetime
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("auto_commit.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("auto_commit")

def run_command(command):
    """Run a shell command and return the output."""
    try:
        process = subprocess.run(
            command, 
            shell=True, 
            check=True, 
            capture_output=True, 
            text=True
        )
        return process.stdout.strip()
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed: {command}")
        logger.error(f"Error: {e.stderr}")
        return None

def get_git_status():
    """Check if there are any changes to commit."""
    return run_command("git status --porcelain")

def commit_changes(message=None):
    """Commit changes to the repository."""
    if message is None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"Auto-commit: Update documentation at {timestamp}"
    
    # Stage all changes
    stage_result = run_command("git add --all")
    if stage_result is None:
        return False
    
    # Commit changes
    commit_result = run_command(f'git commit -m "{message}"')
    if commit_result is None:
        return False
    
    logger.info(f"Changes committed: {message}")
    return True

def push_changes():
    """Push commits to the remote repository."""
    push_result = run_command("git push")
    if push_result is None:
        logger.error("Failed to push changes")
        return False
    
    logger.info("Changes pushed to remote repository")
    return True

def auto_commit_changes(path_to_watch="docs", interval=300):
    """
    Monitor the specified directory and automatically commit and push changes.
    
    Args:
        path_to_watch: Directory to monitor for changes
        interval: Time in seconds between checks
    """
    logger.info(f"Monitoring {path_to_watch} for changes every {interval} seconds")
    
    while True:
        status = get_git_status()
        
        if status:
            logger.info("Changes detected")
            if commit_changes():
                push_changes()
        else:
            logger.info("No changes detected")
        
        time.sleep(interval)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Auto-commit changes to documentation"
    )
    parser.add_argument(
        "--path", 
        default="docs", 
        help="Path to monitor for changes (default: docs)"
    )
    parser.add_argument(
        "--interval", 
        type=int, 
        default=300, 
        help="Interval between checks in seconds (default: 300)"
    )
    parser.add_argument(
        "--commit-only", 
        action="store_true", 
        help="Commit once and exit (don't monitor)"
    )
    
    args = parser.parse_args()
    
    if args.commit_only:
        status = get_git_status()
        if status:
            if commit_changes():
                push_changes()
            else:
                logger.error("Failed to commit changes")
        else:
            logger.info("No changes to commit")
    else:
        auto_commit_changes(args.path, args.interval)
