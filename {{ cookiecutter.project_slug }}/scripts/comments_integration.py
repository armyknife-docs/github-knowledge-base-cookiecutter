#!/usr/bin/env python3
"""
Comments integration for MkDocs knowledge base.
This script adds comment system integration to MkDocs pages.
"""

import os
import re
import json
import logging
import argparse
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("comments_integration")

# Templates for different comment systems
COMMENT_SYSTEMS = {
    "disqus": {
        "description": "Disqus commenting system",
        "js_template": """
<div id="disqus_thread"></div>
<script>
    var disqus_config = function () {
        this.page.url = window.location.href;
        this.page.identifier = '{{page_identifier}}';
    };
    (function() {
        var d = document, s = d.createElement('script');
        s.src = 'https://{{shortname}}.disqus.com/embed.js';
        s.setAttribute('data-timestamp', +new Date());
        (d.head || d.body).appendChild(s);
    })();
</script>
<noscript>Please enable JavaScript to view the <a href="https://disqus.com/?ref_noscript">comments powered by Disqus.</a></noscript>
"""
    },
    "utterances": {
        "description": "Utterances GitHub-based commenting system",
        "js_template": """
<script src="https://utteranc.es/client.js"
        repo="{{repo}}"
        issue-term="pathname"
        theme="github-light"
        crossorigin="anonymous"
        async>
</script>
"""
    },
    "giscus": {
        "description": "Giscus GitHub Discussions-based commenting system",
        "js_template": """
<script src="https://giscus.app/client.js"
        data-repo="{{repo}}"
        data-repo-id="{{repo_id}}"
        data-category="{{category}}"
        data-category-id="{{category_id}}"
        data-mapping="pathname"
        data-reactions-enabled="1"
        data-emit-metadata="0"
        data-theme="light"
        crossorigin="anonymous"
        async>
</script>
"""
    },
    "isso": {
        "description": "Isso self-hosted commenting system",
        "js_template": """
<section id="isso-thread"></section>
<script data-isso="{{isso_url}}" src="{{isso_url}}js/embed.min.js"></script>
"""
    }
}

def generate_comments_integration(system, config, output_dir):
    """
    Generate comments integration for MkDocs.
    
    Args:
        system: Comment system to use (disqus, utterances, giscus, isso)
        config: Dictionary with configuration values
        output_dir: Directory to write integration files
    """
    if system not in COMMENT_SYSTEMS:
        logger.error(f"Unknown comment system: {system}")
        return False
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Create the comments partial template
    template = COMMENT_SYSTEMS[system]["js_template"]
    
    # Replace placeholders with configuration values
    for key, value in config.items():
        template = template.replace(f"{{{{{key}}}}}", value)
    
    # Write the comments template
    comments_file = output_path / "comments.html"
    comments_file.write_text(template)
    logger.info(f"Generated comments integration: {comments_file}")
    
    # Create the JavaScript loader
    loader_js = """
// Comments loader
document.addEventListener('DOMContentLoaded', function() {
    // Find the container to append comments to
    const contentContainer = document.querySelector('.md-content__inner');
    
    if (contentContainer) {
        // Create a container for comments
        const commentsContainer = document.createElement('div');
        commentsContainer.className = 'comments-container';
        commentsContainer.innerHTML = `<h2>Comments</h2>`;
        
        // Load the comments template
        fetch('./comments.html')
            .then(response => response.text())
            .then(html => {
                commentsContainer.innerHTML += html;
                contentContainer.appendChild(commentsContainer);
            })
            .catch(error => {
                console.error('Error loading comments:', error);
            });
    }
});
"""
    
    # Write the loader JavaScript
    loader_file = output_path / "comments-loader.js"
    loader_file.write_text(loader_js)
    logger.info(f"Generated comments loader: {loader_file}")
    
    # Create custom CSS for comments
    comments_css = """
/* Comments styling */
.comments-container {
    margin-top: 3rem;
    padding-top: 1.5rem;
    border-top: 1px solid rgba(0, 0, 0, 0.1);
}

.comments-container h2 {
    margin-bottom: 1.5rem;
    font-size: 1.5rem;
}

.dark-mode .comments-container {
    border-top-color: rgba(255, 255, 255, 0.1);
}
"""
    
    # Write the CSS
    css_file = output_path / "comments.css"
    css_file.write_text(comments_css)
    logger.info(f"Generated comments CSS: {css_file}")
    
    # Generate mkdocs.yml configuration snippet
    mkdocs_config = f"""
# Add this to your mkdocs.yml to enable comments

extra_javascript:
  - js/comments-loader.js

extra_css:
  - css/comments.css
"""
    
    # Write the mkdocs config snippet
    config_file = output_path / "mkdocs-comments-config.yml"
    config_file.write_text(mkdocs_config)
    logger.info(f"Generated MkDocs config snippet: {config_file}")
    
    # Create installation instructions
    instructions = f"""# {system.capitalize()} Comments Integration

To add {system} comments to your MkDocs knowledge base, follow these steps:

1. Copy the following files to your MkDocs project:
   - `comments.html` → `docs/comments.html`
   - `comments-loader.js` → `docs/js/comments-loader.js`
   - `comments.css` → `docs/css/comments.css`

2. Add the configuration from `mkdocs-comments-config.yml` to your `mkdocs.yml` file.

3. Build your MkDocs site as usual.

Your comment section will appear at the bottom of each page.

## Configuration

You've configured {system} with the following settings:

```
{json.dumps(config, indent=2)}
```

To change these settings, regenerate the integration files with new configuration values.
"""
    
    # Write the instructions
    instructions_file = output_path / "INSTRUCTIONS.md"
    instructions_file.write_text(instructions)
    logger.info(f"Generated instructions: {instructions_file}")
    
    return True

def main():
    """Main function to handle command-line arguments and generate integration."""
    parser = argparse.ArgumentParser(
        description="Generate comments integration for MkDocs knowledge base"
    )
    parser.add_argument(
        "--system", "-s",
        choices=list(COMMENT_SYSTEMS.keys()),
        required=True,
        help="Comment system to integrate"
    )
    parser.add_argument(
        "--output", "-o",
        default="comments-integration",
        help="Output directory for integration files"
    )
    parser.add_argument(
        "--config", "-c",
        required=True,
        help="JSON file with configuration values"
    )
    
    args = parser.parse_args()
    
    # Load configuration values
    try:
        with open(args.config, 'r') as f:
            config = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        logger.error(f"Error loading configuration: {e}")
        return 1
    
    # Generate comments integration
    if not generate_comments_integration(args.system, config, args.output):
        return 1
    
    # Output usage instructions
    logger.info(f"Comments integration generated in {args.output}/")
    logger.info(f"Follow the instructions in {args.output}/INSTRUCTIONS.md to complete the setup")
    
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
