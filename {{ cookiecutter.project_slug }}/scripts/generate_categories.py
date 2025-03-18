#!/usr/bin/env python3
"""
Script to generate category pages by scanning all markdown files
and organizing them by their category tags.
"""

import os
import re
import yaml
import logging
from pathlib import Path
from collections import defaultdict

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("generate_categories")

def extract_frontmatter(content):
    """Extract YAML frontmatter from markdown content."""
    frontmatter_match = re.match(r'^---\s+(.*?)\s+---', content, re.DOTALL)
    if frontmatter_match:
        try:
            frontmatter_content = frontmatter_match.group(1)
            return yaml.safe_load(frontmatter_content)
        except yaml.YAMLError as e:
            logger.warning(f"Error parsing frontmatter: {e}")
    return {}

def extract_title(content):
    """Extract the first heading as the document title."""
    title_match = re.search(r'^#\s+(.*?)$', content, re.MULTILINE)
    if title_match:
        return title_match.group(1)
    return "Untitled"

def scan_docs_directory(docs_dir):
    """
    Scan the docs directory for markdown files, extract categories
    from frontmatter, and organize files by category.
    """
    categories = defaultdict(list)
    docs_path = Path(docs_dir)
    
    for file_path in docs_path.glob('**/*.md'):
        # Skip the tags and categories pages themselves
        if file_path.name == 'tags.md' or file_path.parent.name == 'categories':
            continue
        
        rel_path = file_path.relative_to(docs_path)
        content = file_path.read_text()
        
        frontmatter = extract_frontmatter(content)
        title = extract_title(content)
        
        # Check for category in frontmatter
        if 'category' in frontmatter:
            category_name = frontmatter['category']
            if isinstance(category_name, list):
                for cat in category_name:
                    categories[cat].append((str(rel_path), title))
            else:
                categories[category_name].append((str(rel_path), title))
        
        # Also check for category syntax in the content
        category_match = re.search(r'{{category:\s*(.*?)\s*}}', content)
        if category_match:
            category_name = category_match.group(1)
            categories[category_name].append((str(rel_path), title))
    
    return categories

def generate_category_pages(docs_dir, categories):
    """
    Generate a markdown page for each category listing all documents.
    """
    categories_dir = Path(docs_dir) / 'categories'
    categories_dir.mkdir(exist_ok=True)
    
    # Create an index page for all categories
    index_content = "# Categories\n\nBrowse documentation by category:\n\n"
    
    for category_name, documents in sorted(categories.items()):
        # Create slug from category name
        category_slug = category_name.lower().replace(' ', '-')
        category_file = categories_dir / f"{category_slug}.md"
        
        # Generate the category page content
        content = f"# {category_name}\n\nThe following documents are categorized as **{category_name}**:\n\n"
        
        for doc_path, doc_title in sorted(documents):
            content += f"- [{doc_title}](../{doc_path})\n"
        
        # Write the category page
        category_file.write_text(content)
        logger.info(f"Generated category page: {category_file}")
        
        # Add to index
        index_content += f"- [{category_name}](categories/{category_slug}.md) ({len(documents)} documents)\n"
    
    # Write the categories index page
    index_file = Path(docs_dir) / 'categories' / 'index.md'
    index_file.write_text(index_content)
    logger.info(f"Generated categories index: {index_file}")

def main():
    """Main function to scan docs and generate category pages."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Generate category pages from markdown frontmatter"
    )
    parser.add_argument(
        "--docs-dir", 
        default="docs", 
        help="Path to the docs directory"
    )
    
    args = parser.parse_args()
    
    # Scan the docs directory
    categories = scan_docs_directory(args.docs_dir)
    
    if categories:
        # Generate category pages
        generate_category_pages(args.docs_dir, categories)
        logger.info(f"Generated {len(categories)} category pages")
    else:
        logger.warning("No categories found in the documentation")

if __name__ == "__main__":
    main()
