#!/usr/bin/env python3
"""
Script to set up Git hooks for the repository.
"""

import os
import sys
import logging
from pathlib import Path
import stat

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("setup_hooks")

def create_pre_commit_hook():
    """Create a pre-commit hook to validate markdown files."""
    git_dir = Path(".git")
    hooks_dir = git_dir / "hooks"
    
    if not git_dir.exists():
        logger.error("Not a git repository (or .git directory not found)")
        return False
    
    pre_commit_path = hooks_dir / "pre-commit"
    
    pre_commit_content = """#!/bin/sh
#
# Pre-commit hook to validate markdown files
#

# Run markdownlint on staged markdown files
staged_md_files=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\\.md$')

if [ -n "$staged_md_files" ]; then
    echo "Running markdown lint on staged files..."
    npx markdownlint-cli $staged_md_files
    if [ $? -ne 0 ]; then
        echo "Markdown validation failed. Fix the issues before committing."
        exit 1
    fi
fi

# Success
exit 0
"""
    
    # Write the pre-commit hook
    pre_commit_path.write_text(pre_commit_content)
    
    # Make the hook executable
    pre_commit_path.chmod(pre_commit_path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    
    logger.info(f"Created pre-commit hook: {pre_commit_path}")
    return True

def create_post_commit_hook():
    """Create a post-commit hook to generate and deploy documentation."""
    git_dir = Path(".git")
    hooks_dir = git_dir / "hooks"
    
    if not git_dir.exists():
        logger.error("Not a git repository (or .git directory not found)")
        return False
    
    post_commit_path = hooks_dir / "post-commit"
    
    post_commit_content = """#!/bin/sh
#
# Post-commit hook to generate and deploy documentation
#

# Only run on the main branch
current_branch=$(git symbolic-ref --short HEAD)
if [ "$current_branch" != "main" ] && [ "$current_branch" != "master" ]; then
    exit 0
fi

# Check if any markdown files were changed
md_files_changed=$(git diff-tree --no-commit-id --name-only -r HEAD | grep -E '\\.md$')
if [ -z "$md_files_changed" ]; then
    exit 0
fi

echo "Markdown files changed, rebuilding documentation..."

# Build the documentation
if command -v mkdocs &> /dev/null; then
    mkdocs build
    echo "Documentation rebuilt successfully."
else
    echo "Warning: mkdocs not found, skipping documentation build."
fi

exit 0
"""
    
    # Write the post-commit hook
    post_commit_path.write_text(post_commit_content)
    
    # Make the hook executable
    post_commit_path.chmod(post_commit_path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    
    logger.info(f"Created post-commit hook: {post_commit_path}")
    return True

def setup_hooks():
    """Set up all Git hooks for the repository."""
    success = True
    
    if not create_pre_commit_hook():
        success = False
    
    if not create_post_commit_hook():
        success = False
    
    return success

if __name__ == "__main__":
    if setup_hooks():
        logger.info("Git hooks set up successfully")
        sys.exit(0)
    else:
        logger.error("Failed to set up Git hooks")
        sys.exit(1)
