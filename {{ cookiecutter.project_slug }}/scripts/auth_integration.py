#!/usr/bin/env python3
"""
Authentication integration for a self-hosted MkDocs knowledge base.
This script provides integration with common authentication systems
for private knowledge bases.
"""

import os
import json
import logging
import argparse
import subprocess
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("auth_integration")

# Templates for authentication configurations
AUTH_CONFIGS = {
    "nginx": {
        "description": "Nginx basic authentication configuration",
        "template": """
# Nginx basic auth configuration
# Place this in your server block
location / {
    auth_basic "Restricted Knowledge Base";
    auth_basic_user_file /etc/nginx/.htpasswd;
    try_files $uri $uri/ =404;
}
""",
        "help": """
To use this configuration:
1. Install apache2-utils: `apt-get install apache2-utils`
2. Create password file: `htpasswd -c /etc/nginx/.htpasswd username`
3. Add the configuration to your Nginx server block
4. Reload Nginx: `nginx -s reload`
"""
    },
    "htaccess": {
        "description": "Apache .htaccess authentication",
        "template": """
# Apache .htaccess authentication
AuthType Basic
AuthName "Restricted Knowledge Base"
AuthUserFile /path/to/.htpasswd
Require valid-user
""",
        "help": """
To use this configuration:
1. Create password file: `htpasswd -c /path/to/.htpasswd username`
2. Place this .htaccess file in your site directory
3. Ensure Apache is configured to allow .htaccess overrides
"""
    },
    "oauth2-proxy": {
        "description": "OAuth2 Proxy for Google/GitHub authentication",
        "template": """
# OAuth2 Proxy configuration
provider = "google"
client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"
cookie_secret = "GENERATE_COOKIE_SECRET"
email_domains = ["yourdomain.com"]
upstream = "http://localhost:8000"
""",
        "help": """
To use OAuth2 Proxy:
1. Install OAuth2 Proxy: https://oauth2-proxy.github.io/oauth2-proxy/
2. Set up OAuth credentials in Google Cloud Console or GitHub
3. Generate a cookie secret: `openssl rand -base64 32`
4. Update the configuration with your details
5. Run OAuth2 Proxy in front of your MkDocs server
"""
    },
    "keycloak": {
        "description": "Keycloak integration for enterprise authentication",
        "template": """
# Keycloak integration settings
{
  "realm": "knowledge-base",
  "auth-server-url": "https://keycloak.yourdomain.com/auth",
  "ssl-required": "external",
  "resource": "knowledge-base-client",
  "public-client": true,
  "confidential-port": 0
}
""",
        "help": """
To use Keycloak integration:
1. Set up a Keycloak server
2. Create a new realm and client for your knowledge base
3. Configure the client settings to match your deployment
4. Use keycloak-httpd-client-install to configure your web server
"""
    }
}

def generate_auth_config(auth_type, output_dir, config_values=None):
    """
    Generate authentication configuration files.
    
    Args:
        auth_type: Type of authentication (nginx, htaccess, oauth2-proxy, keycloak)
        output_dir: Directory to write configuration files
        config_values: Optional dictionary of values to substitute in the template
    """
    if auth_type not in AUTH_CONFIGS:
        logger.error(f"Unknown authentication type: {auth_type}")
        return False
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    config = AUTH_CONFIGS[auth_type]
    template = config["template"]
    
    # Substitute values in the template if provided
    if config_values:
        for key, value in config_values.items():
            template = template.replace(f"YOUR_{key.upper()}", value)
    
    # Write the configuration file
    if auth_type == "nginx":
        output_file = output_path / "nginx-auth.conf"
    elif auth_type == "htaccess":
        output_file = output_path / ".htaccess"
    elif auth_type == "oauth2-proxy":
        output_file = output_path / "oauth2-proxy.cfg"
    elif auth_type == "keycloak":
        output_file = output_path / "keycloak.json"
    
    output_file.write_text(template.strip())
    logger.info(f"Generated {auth_type} configuration: {output_file}")
    
    # Write help file
    help_file = output_path / f"{auth_type}-auth-help.txt"
    help_file.write_text(config["help"].strip())
    logger.info(f"Generated help file: {help_file}")
    
    return True

def setup_auth_users(auth_type, output_dir, users):
    """
    Set up authentication users for basic auth.
    
    Args:
        auth_type: Type of authentication (nginx, htaccess)
        output_dir: Directory to write password files
        users: List of username:password pairs
    """
    if auth_type not in ["nginx", "htaccess"]:
        logger.warning(f"User setup not supported for {auth_type}")
        return False
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    htpasswd_file = output_path / ".htpasswd"
    
    try:
        # Try to use htpasswd command if available
        for user_pass in users:
            username, password = user_pass.split(":", 1)
            
            if htpasswd_file.exists() and users.index(user_pass) == 0:
                # Create new file for first user
                subprocess.run(
                    ["htpasswd", "-cb", str(htpasswd_file), username, password],
                    check=True, 
                    capture_output=True
                )
            else:
                # Append additional users
                subprocess.run(
                    ["htpasswd", "-b", str(htpasswd_file), username, password],
                    check=True, 
                    capture_output=True
                )
                
        logger.info(f"Created htpasswd file with {len(users)} users: {htpasswd_file}")
        return True
        
    except (subprocess.SubprocessError, FileNotFoundError):
        logger.warning("htpasswd command not available, creating manual example")
        
        # Create an example file instead
        example_file = output_path / "htpasswd-example.txt"
        example_file.write_text(
            "# Example .htpasswd file\n"
            "# Generate real entries using: htpasswd -nb username password\n"
            "# or online generators\n"
            + "\n".join([f"{user.split(':', 1)[0]}:$apr1$EXAMPLE-HASH" for user in users])
        )
        
        logger.info(f"Created example htpasswd file: {example_file}")
        return False

def main():
    """Main function to handle command-line arguments and generate configs."""
    parser = argparse.ArgumentParser(
        description="Generate authentication configurations for MkDocs knowledge base"
    )
    parser.add_argument(
        "--type", "-t",
        choices=list(AUTH_CONFIGS.keys()),
        required=True,
        help="Type of authentication to configure"
    )
    parser.add_argument(
        "--output", "-o",
        default="auth-config",
        help="Output directory for configuration files"
    )
    parser.add_argument(
        "--users", "-u",
        nargs="+",
        help="Users to add in username:password format (for basic auth)"
    )
    parser.add_argument(
        "--values", "-v",
        help="JSON file with configuration values"
    )
    
    args = parser.parse_args()
    
    # Load configuration values if provided
    config_values = None
    if args.values:
        try:
            with open(args.values, 'r') as f:
                config_values = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            logger.error(f"Error loading configuration values: {e}")
            return 1
    
    # Generate authentication configuration
    if not generate_auth_config(args.type, args.output, config_values):
        return 1
    
    # Set up users if applicable
    if args.users and args.type in ["nginx", "htaccess"]:
        setup_auth_users(args.type, args.output, args.users)
    
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
