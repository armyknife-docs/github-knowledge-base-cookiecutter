#!/usr/bin/env python3
"""
Custom hooks for MkDocs processing.
Handles tags processing and category organization.
"""

import re
import yaml
from pathlib import Path

def get_tags_from_frontmatter(markdown):
    """Extract tags from the frontmatter of markdown content."""
    tags = []
    
    # Match YAML frontmatter between --- markers
    frontmatter_match = re.match(r'^---\s+(.*?)\s+---', markdown, re.DOTALL)
    if frontmatter_match:
        try:
            frontmatter_content = frontmatter_match.group(1)
            frontmatter = yaml.safe_load(frontmatter_content)
            
            if frontmatter and 'tags' in frontmatter:
                # Handle both string format and list format
                if isinstance(frontmatter['tags'], str):
                    # Split comma-separated tags and strip whitespace
                    tags = [tag.strip() for tag in frontmatter['tags'].split(',') if tag.strip()]
                elif isinstance(frontmatter['tags'], list):
                    tags = frontmatter['tags']
        except yaml.YAMLError:
            pass
    
    return tags

def generate_tag_links(tags):
    """Generate markdown links for tags."""
    if not tags:
        return ""
    
    tag_links = [f"[{tag}](../tags.md#{tag.lower().replace(' ', '-')})" for tag in tags]
    return "<div class='tag-container'>" + " ".join(tag_links) + "</div>"

def on_page_markdown(markdown, page, config, files):
    """
    Process markdown content before MkDocs renders it.
    
    This hook:
    1. Extracts tags from frontmatter
    2. Adds tag links at the top of the document
    3. Processes any special category syntax
    """
    tags = get_tags_from_frontmatter(markdown)
    
    if tags:
        # Add tag links after the first heading
        heading_match = re.search(r'^#\s+.*$', markdown, re.MULTILINE)
        if heading_match:
            heading_end = heading_match.end()
            tag_section = f"\n\n{generate_tag_links(tags)}\n"
            markdown = markdown[:heading_end] + tag_section + markdown[heading_end:]
    
    # Process category syntax - optional feature that uses a custom syntax like 
    # {{category: Development}} to indicate a category
    category_match = re.search(r'{{category:\s*(.*?)\s*}}', markdown)
    if category_match:
        category = category_match.group(1)
        category_link = f"**Category:** [{category}](../categories/{category.lower().replace(' ', '-')}.md)"
        markdown = re.sub(r'{{category:\s*(.*?)\s*}}', category_link, markdown)
    
    return markdown
