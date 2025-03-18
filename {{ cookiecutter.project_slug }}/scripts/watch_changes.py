#!/usr/bin/env python3
"""
File watcher script that monitors changes in the docs directory and 
triggers the auto_commit.py script when files are changed.
"""

import os
import sys
import time
import logging
import subprocess
from pathlib import Path
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("file_watcher.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("file_watcher")

class ChangeHandler(FileSystemEventHandler):
    """Handle file system events like file creation, modification, etc."""
    
    def __init__(self, debounce_time=5):
        """
        Initialize the change handler.
        
        Args:
            debounce_time: Time in seconds to wait after the last change
                           before triggering a commit
        """
        self.debounce_time = debounce_time
        self.last_modified = datetime.now()
        self.timer_running = False
    
    def on_any_event(self, event):
        """Handle any file system event."""
        # Ignore directory creation events and hidden files
        if event.is_directory or os.path.basename(event.src_path).startswith('.'):
            return
        
        logger.info(f"Change detected: {event.src_path} ({event.event_type})")
        self.last_modified = datetime.now()
        
        if not self.timer_running:
            self.timer_running = True
            self._start_timer()
    
    def _start_timer(self):
        """Start a timer to wait for changes to settle before committing."""
        while True:
            time_since_last_change = (datetime.now() - self.last_modified).total_seconds()
            
            if time_since_last_change >= self.debounce_time:
                logger.info(f"Changes settled after {self.debounce_time} seconds")
                self._trigger_commit()
                self.timer_running = False
                break
            
            time.sleep(1)
    
    def _trigger_commit(self):
        """Trigger the auto_commit.py script."""
        logger.info("Triggering auto commit")
        
        script_dir = Path(__file__).parent.absolute()
        commit_script = script_dir / "auto_commit.py"
        
        try:
            subprocess.run(
                [sys.executable, str(commit_script), "--commit-only"],
                check=True
            )
            logger.info("Auto commit completed successfully")
        except subprocess.CalledProcessError as e:
            logger.error(f"Auto commit failed: {e}")

def watch_directory(path_to_watch="docs", debounce_time=5):
    """
    Watch the specified directory for changes.
    
    Args:
        path_to_watch: Directory to monitor for changes
        debounce_time: Time in seconds to wait after the last change
                      before triggering a commit
    """
    path = Path(path_to_watch).absolute()
    logger.info(f"Starting file watcher for {path}")
    
    event_handler = ChangeHandler(debounce_time)
    observer = Observer()
    observer.schedule(event_handler, str(path), recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    
    observer.join()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Watch for changes in the documentation directory"
    )
    parser.add_argument(
        "--path", 
        default="docs", 
        help="Path to monitor for changes (default: docs)"
    )
    parser.add_argument(
        "--debounce", 
        type=int, 
        default=5, 
        help="Debounce time in seconds (default: 5)"
    )
    
    args = parser.parse_args()
    watch_directory(args.path, args.debounce)
