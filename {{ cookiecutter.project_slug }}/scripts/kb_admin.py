#!/usr/bin/env python3
"""
Knowledge Base Administration Script.
This script provides a unified interface for managing all aspects of the
GitHub Knowledge Base system.
"""

import os
import sys
import subprocess
import logging
import argparse
from pathlib import Path
import importlib
import shutil

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("kb_admin")

class KnowledgeBaseAdmin:
    """
    Admin utility for managing all aspects of the knowledge base.
    """
    
    def __init__(self, base_dir="."):
        """
        Initialize the admin utility.
        
        Args:
            base_dir: Base directory of the knowledge base
        """
        self.base_dir = Path(base_dir).absolute()
        self.docs_dir = self.base_dir / "docs"
        self.scripts_dir = self.base_dir / "scripts"
        
        # Ensure we're in a knowledge base directory
        if not self._is_knowledge_base():
            logger.warning(f"Warning: {self.base_dir} may not be a knowledge base directory")
    
    def _is_knowledge_base(self):
        """Check if the current directory is a knowledge base."""
        return (self.base_dir / "mkdocs.yml").exists() and self.docs_dir.exists()
    
    def _import_module(self, module_path):
        """
        Dynamically import a module from a file path.
        
        Args:
            module_path: Path to the Python module to import
            
        Returns:
            The imported module object or None if import fails
        """
        try:
            module_name = module_path.stem
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
        except (ImportError, AttributeError) as e:
            logger.error(f"Error importing module {module_path}: {e}")
            return None
    
    def _run_script(self, script_name, args=None):
        """
        Run a Python script with arguments.
        
        Args:
            script_name: Name of the script to run
            args: List of arguments to pass to the script
            
        Returns:
            True if the script succeeds, False otherwise
        """
        script_path = self.scripts_dir / f"{script_name}.py"
        
        if not script_path.exists():
            logger.error(f"Script {script_path} not found")
            return False
        
        cmd = [sys.executable, str(script_path)]
        if args:
            cmd.extend(args)
        
        try:
            subprocess.run(cmd, check=True)
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Error running script {script_name}: {e}")
            return False
    
    def create_document(self, title, description=None, author=None, tags=None, category=None):
        """
        Create a new document in the knowledge base.
        
        Args:
            title: Document title
            description: Document description
            author: Document author
            tags: Comma-separated list of tags
            category: Document category
            
        Returns:
            True if the document was created, False otherwise
        """
        args = [title]
        
        if description:
            args.extend(["--desc", description])
        
        if author:
            args.extend(["--author", author])
        
        if tags:
            args.extend(["--tags", tags])
        
        if category:
            args.extend(["--category", category])
        
        return self._run_script("create_document", args)
    
    def start_watcher(self, interval=5):
        """
        Start the file watcher for automatic commits.
        
        Args:
            interval: Debounce interval in seconds
            
        Returns:
            True if the watcher was started, False otherwise
        """
        return self._run_script("watch_changes", ["--debounce", str(interval)])
    
    def build_site(self):
        """
        Build the MkDocs site.
        
        Returns:
            True if the site was built, False otherwise
        """
        try:
            subprocess.run(["mkdocs", "build"], check=True)
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Error building site: {e}")
            return False
    
    def serve_site(self, port=8000):
        """
        Start the MkDocs development server.
        
        Args:
            port: Port to serve on
            
        Returns:
            True if the server started, False otherwise
        """
        try:
            subprocess.run(["mkdocs", "serve", "--port", str(port)], check=True)
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Error serving site: {e}")
            return False
    
    def deploy_site(self):
        """
        Deploy the site to GitHub Pages.
        
        Returns:
            True if the site was deployed, False otherwise
        """
        try:
            subprocess.run(["mkdocs", "gh-deploy", "--force"], check=True)
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Error deploying site: {e}")
            return False
    
    def setup_git_hooks(self):
        """
        Set up Git hooks for the repository.
        
        Returns:
            True if the hooks were set up, False otherwise
        """
        return self._run_script("setup_hooks")
    
    def generate_tags(self):
        """
        Generate tags pages by scanning the documentation.
        
        Returns:
            True if the tags were generated, False otherwise
        """
        # First try to use the generate_tags script if it exists
        if (self.scripts_dir / "generate_tags.py").exists():
            return self._run_script("generate_tags")
        
        # Otherwise, try to use MkDocs tags plugin
        try:
            # Create tags template if it doesn't exist
            tags_file = self.docs_dir / "tags.md"
            if not tags_file.exists():
                tags_file.write_text("# Tags\n\nBrowse documentation by tag:\n\n[TAGS]")
                logger.info(f"Created tags template: {tags_file}")
            
            # Build site to generate tags
            subprocess.run(["mkdocs", "build"], check=True)
            logger.info("Generated tags by building the site")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Error generating tags: {e}")
            return False
    
    def generate_categories(self):
        """
        Generate category pages by scanning the documentation.
        
        Returns:
            True if the categories were generated, False otherwise
        """
        if (self.scripts_dir / "generate_categories.py").exists():
            return self._run_script("generate_categories")
        else:
            logger.error("generate_categories.py script not found")
            return False
    
    def setup_comments(self, system, config_file):
        """
        Set up a comments system for the knowledge base.
        
        Args:
            system: Comments system to use
            config_file: Path to comments configuration file
            
        Returns:
            True if the comments system was set up, False otherwise
        """
        # Try to use existing script if it exists
        if (self.scripts_dir / "comments_integration.py").exists():
            return self._run_script("comments_integration", [
                "--system", system,
                "--config", config_file
            ])
        
        # Try to import the comments integration module from lib
        comments_module_path = Path(__file__).parent / "lib" / "comments_integration.py"
        if comments_module_path.exists():
            module = self._import_module(comments_module_path)
            if module:
                try:
                    with open(config_file, 'r') as f:
                        config = json.load(f)
                    
                    output_dir = self.base_dir / "comments-integration"
                    result = module.generate_comments_integration(system, config, output_dir)
                    
                    if result:
                        logger.info(f"Generated comments integration in {output_dir}")
                        logger.info(f"Follow the instructions in {output_dir}/INSTRUCTIONS.md")
                        return True
                except Exception as e:
                    logger.error(f"Error setting up comments: {e}")
        
        logger.error("Comments integration script not found")
        return False
    
    def setup_analytics(self, system, config_file):
        """
        Set up analytics for the knowledge base.
        
        Args:
            system: Analytics system to use
            config_file: Path to analytics configuration file
            
        Returns:
            True if the analytics system was set up, False otherwise
        """
        # Try to use existing script if it exists
        if (self.scripts_dir / "analytics_integration.py").exists():
            return self._run_script("analytics_integration", [
                "--system", system,
                "--config", config_file
            ])
        
        # Try to import the analytics integration module from lib
        analytics_module_path = Path(__file__).parent / "lib" / "analytics_integration.py"
        if analytics_module_path.exists():
            module = self._import_module(analytics_module_path)
            if module:
                try:
                    with open(config_file, 'r') as f:
                        config = json.load(f)
                    
                    output_dir = self.base_dir / "analytics-integration"
                    result = module.generate_analytics_integration(system, config, output_dir)
                    
                    if result:
                        logger.info(f"Generated analytics integration in {output_dir}")
                        logger.info(f"Follow the instructions in {output_dir}/INSTRUCTIONS.md")
                        return True
                except Exception as e:
                    logger.error(f"Error setting up analytics: {e}")
        
        logger.error("Analytics integration script not found")
        return False
    
    def setup_auth(self, auth_type, config_file=None, users=None):
        """
        Set up authentication for the knowledge base.
        
        Args:
            auth_type: Type of authentication to set up
            config_file: Path to authentication configuration file
            users: List of username:password pairs for basic auth
            
        Returns:
            True if the authentication system was set up, False otherwise
        """
        # Try to use existing script if it exists
        args = ["--type", auth_type]
        
        if config_file:
            args.extend(["--values", config_file])
        
        if users:
            args.extend(["--users"])
            args.extend(users)
        
        if (self.scripts_dir / "auth_integration.py").exists():
            return self._run_script("auth_integration", args)
        
        logger.error("Authentication integration script not found")
        return False
    
    def create_backup(self, output_dir=None):
        """
        Create a backup of the knowledge base.
        
        Args:
            output_dir: Directory to store the backup
            
        Returns:
            Path to the backup file or None if backup failed
        """
        import datetime
        import zipfile
        
        # Get the current date and time
        now = datetime.datetime.now()
        date_str = now.strftime("%Y%m%d_%H%M%S")
        
        # Determine backup location
        if output_dir:
            backup_dir = Path(output_dir)
        else:
            backup_dir = self.base_dir.parent / "backups"
        
        # Create backup directory if it doesn't exist
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Create backup filename
        backup_file = backup_dir / f"{self.base_dir.name}_{date_str}.zip"
        
        try:
            # Create zip archive
            with zipfile.ZipFile(backup_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Add all files except .git directory
                for root, dirs, files in os.walk(self.base_dir):
                    # Skip .git directory
                    if '.git' in dirs:
                        dirs.remove('.git')
                    
                    # Skip site directory (generated by MkDocs)
                    if 'site' in dirs:
                        dirs.remove('site')
                    
                    for file in files:
                        file_path = os.path.join(root, file)
                        rel_path = os.path.relpath(file_path, self.base_dir)
                        zipf.write(file_path, rel_path)
            
            logger.info(f"Backup created: {backup_file}")
            return backup_file
        
        except Exception as e:
            logger.error(f"Error creating backup: {e}")
            return None

def main():
    """Main entry point for the admin script."""
    parser = argparse.ArgumentParser(
        description="Knowledge Base Administration Tool"
    )
    parser.add_argument(
        "--dir", "-d",
        default=".",
        help="Knowledge base directory (default: current directory)"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Document creation command
    doc_parser = subparsers.add_parser("create-doc", help="Create a new document")
    doc_parser.add_argument("title", help="Document title")
    doc_parser.add_argument("--desc", help="Document description")
    doc_parser.add_argument("--author", help="Document author")
    doc_parser.add_argument("--tags", help="Comma-separated list of tags")
    doc_parser.add_argument("--category", help="Document category")
    
    # File watcher command
    watch_parser = subparsers.add_parser("watch", help="Start file watcher for auto-commits")
    watch_parser.add_argument("--interval", type=int, default=5, help="Debounce interval in seconds")
    
    # Site commands
    subparsers.add_parser("build", help="Build the MkDocs site")
    
    serve_parser = subparsers.add_parser("serve", help="Start the MkDocs development server")
    serve_parser.add_argument("--port", type=int, default=8000, help="Port to serve on")
    
    subparsers.add_parser("deploy", help="Deploy the site to GitHub Pages")
    
    # Setup commands
    subparsers.add_parser("setup-hooks", help="Set up Git hooks")
    subparsers.add_parser("generate-tags", help="Generate tags pages")
    subparsers.add_parser("generate-categories", help="Generate category pages")
    
    # Comments setup command
    comments_parser = subparsers.add_parser("setup-comments", help="Set up comments system")
    comments_parser.add_argument("--system", required=True, choices=["disqus", "utterances", "giscus", "isso"], 
                               help="Comments system to use")
    comments_parser.add_argument("--config", required=True, help="Path to config file")
    
    # Analytics setup command
    analytics_parser = subparsers.add_parser("setup-analytics", help="Set up analytics")
    analytics_parser.add_argument("--system", required=True, 
                                choices=["google-analytics", "plausible", "matomo", "fathom", "umami", "custom-js"], 
                                help="Analytics system to use")
    analytics_parser.add_argument("--config", required=True, help="Path to config file")
    
    # Auth setup command
    auth_parser = subparsers.add_parser("setup-auth", help="Set up authentication")
    auth_parser.add_argument("--type", required=True, 
                          choices=["nginx", "htaccess", "oauth2-proxy", "keycloak"], 
                          help="Authentication type")
    auth_parser.add_argument("--config", help="Path to config file")
    auth_parser.add_argument("--users", nargs="+", help="Username:password pairs for basic auth")
    
    # Backup command
    backup_parser = subparsers.add_parser("backup", help="Create a backup of the knowledge base")
    backup_parser.add_argument("--output", help="Output directory for the backup")
    
    args = parser.parse_args()
    
    # Create admin instance
    admin = KnowledgeBaseAdmin(args.dir)
    
    # Run the appropriate command
    if args.command == "create-doc":
        admin.create_document(args.title, args.desc, args.author, args.tags, args.category)
    
    elif args.command == "watch":
        admin.start_watcher(args.interval)
    
    elif args.command == "build":
        admin.build_site()
    
    elif args.command == "serve":
        admin.serve_site(args.port)
    
    elif args.command == "deploy":
        admin.deploy_site()
    
    elif args.command == "setup-hooks":
        admin.setup_git_hooks()
    
    elif args.command == "generate-tags":
        admin.generate_tags()
    
    elif args.command == "generate-categories":
        admin.generate_categories()
    
    elif args.command == "setup-comments":
        admin.setup_comments(args.system, args.config)
    
    elif args.command == "setup-analytics":
        admin.setup_analytics(args.system, args.config)
    
    elif args.command == "setup-auth":
        admin.setup_auth(args.type, args.config, args.users)
    
    elif args.command == "backup":
        admin.create_backup(args.output)
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()