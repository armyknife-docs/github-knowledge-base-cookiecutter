#!/usr/bin/env python3
"""
Script to create new knowledge base documents with proper formatting and frontmatter.
"""

import os
import sys
import re
import logging
from datetime import datetime
from pathlib import Path
import yaml

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("create_document")

class DocumentCreator:
    """Create and manage knowledge base documents."""
    
    def __init__(self, docs_dir="docs"):
        """
        Initialize the document creator.
        
        Args:
            docs_dir: Path to the docs directory
        """
        self.docs_dir = Path(docs_dir)
        if not self.docs_dir.exists():
            logger.error(f"Docs directory '{docs_dir}' does not exist")
            sys.exit(1)
    
    def slugify(self, text):
        """
        Convert text to a URL-friendly slug.
        
        Args:
            text: The text to convert
            
        Returns:
            A slug version of the text
        """
        # Convert to lowercase and replace spaces with hyphens
        text = text.lower().strip()
        text = re.sub(r'[^\w\s-]', '', text)
        text = re.sub(r'[\s_-]+', '-', text)
        text = re.sub(r'^-+|-+$', '', text)
        return text
    
    def _get_default_template(self):
        """Get the default document template."""
        return """---
title: {title}
description: {description}
created: {date}
updated: {date}
author: {author}
tags: {tags}
---

# {title}

{description}

## Overview

[Add content here]

## Details

[Add details here]

## Related

- [Add related links here]
"""
    
    def create_document(self, title, description="", author="", tags=None, category=None):
        """
        Create a new document with the specified parameters.
        
        Args:
            title: Document title
            description: Document description
            author: Document author
            tags: List of tags
            category: Document category (subfolder)
            
        Returns:
            Path to the created document
        """
        tags = tags or []
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Create slug for filename
        slug = self.slugify(title)
        
        # Determine document path
        if category:
            category_path = self.docs_dir / category
            if not category_path.exists():
                category_path.mkdir(parents=True)
            doc_path = category_path / f"{slug}.md"
        else:
            doc_path = self.docs_dir / f"{slug}.md"
        
        # Check if document already exists
        if doc_path.exists():
            logger.warning(f"Document '{doc_path}' already exists")
            return None
        
        # Create document content
        content = self._get_default_template().format(
            title=title,
            description=description,
            date=date,
            author=author,
            tags=", ".join(tags)
        )
        
        # Write document
        doc_path.write_text(content)
        logger.info(f"Created document: {doc_path}")
        
        return doc_path
    
    def update_mkdocs_nav(self, doc_path):
        """
        Update the mkdocs.yml navigation to include the new document.
        
        Args:
            doc_path: Path to the created document
        """
        # TODO: Implement this functionality to automatically update the mkdocs.yml
        # This is a more complex task that would require parsing and modifying the YAML
        # while preserving its structure and comments
        logger.info("Navigation update is not implemented yet")

def main():
    """Main entry point for the document creator script."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Create a new knowledge base document"
    )
    parser.add_argument(
        "title", 
        help="Document title"
    )
    parser.add_argument(
        "--desc", "-d", 
        dest="description",
        default="", 
        help="Document description"
    )
    parser.add_argument(
        "--author", "-a", 
        default="", 
        help="Document author"
    )
    parser.add_argument(
        "--tags", "-t", 
        default="", 
        help="Comma-separated list of tags"
    )
    parser.add_argument(
        "--category", "-c", 
        default=None, 
        help="Document category (subfolder)"
    )
    parser.add_argument(
        "--docs-dir", 
        default="docs", 
        help="Path to the docs directory"
    )
    
    args = parser.parse_args()
    
    tags = [tag.strip() for tag in args.tags.split(",") if tag.strip()]
    
    creator = DocumentCreator(args.docs_dir)
    doc_path = creator.create_document(
        args.title,
        args.description,
        args.author,
        tags,
        args.category
    )
    
    if doc_path:
        logger.info(f"Document created successfully: {doc_path}")
        # creator.update_mkdocs_nav(doc_path)

if __name__ == "__main__":
    main()
