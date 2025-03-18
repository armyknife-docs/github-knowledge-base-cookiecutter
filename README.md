# {{ cookiecutter.project_name }}

[![GitHub release](https://img.shields.io/github/release/{{ cookiecutter.author_name|lower|replace(" ", "-") }}/{{ cookiecutter.project_slug }}.svg)](https://github.com/{{ cookiecutter.author_name|lower|replace(" ", "-") }}/{{ cookiecutter.project_slug }}/releases)
[![PyPI version](https://img.shields.io/pypi/v/{{ cookiecutter.project_slug }}.svg)](https://pypi.org/project/{{ cookiecutter.project_slug }}/)
[![Build Status](https://github.com/{{ cookiecutter.author_name|lower|replace(" ", "-") }}/{{ cookiecutter.project_slug }}/workflows/CI/badge.svg)](https://github.com/{{ cookiecutter.author_name|lower|replace(" ", "-") }}/{{ cookiecutter.project_slug }}/actions?query=workflow%3ACI)
[![License](https://img.shields.io/badge/License-{{ cookiecutter.open_source_license|replace("-", "--")|replace(" ", "%20") }}-blue.svg)](https://opensource.org/licenses/{{ cookiecutter.open_source_license|replace(" ", "-") }})
[![Python Versions](https://img.shields.io/pypi/pyversions/{{ cookiecutter.project_slug }}.svg)](https://pypi.org/project/{{ cookiecutter.project_slug }}/)
[![Documentation Status](https://readthedocs.org/projects/{{ cookiecutter.project_slug }}/badge/?version=latest)](https://{{ cookiecutter.project_slug }}.readthedocs.io/en/latest/?badge=latest)
[![codecov](https://codecov.io/gh/{{ cookiecutter.author_name|lower|replace(" ", "-") }}/{{ cookiecutter.project_slug }}/branch/main/graph/badge.svg)](https://codecov.io/gh/{{ cookiecutter.author_name|lower|replace(" ", "-") }}/{{ cookiecutter.project_slug }})
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

{{ cookiecutter.project_description }}

---

## 📚 Overview

GitHub Knowledge Base is a powerful, customizable knowledge management system built on MkDocs that integrates seamlessly with your GitHub workflow. It provides a structured approach to create, organize, and share documentation, knowledge articles, and guides within your organization or project.

![Knowledge Base Screenshot](docs/assets/images/screenshot.png)

### Key Features

- 🚀 **MkDocs-powered** - Beautiful, responsive documentation with Material for MkDocs theme
- 🔄 **Git Integration** - Automatically commit and sync changes
- 🏷️ **Advanced Tagging** - Categorize and filter content with tags
- 🔍 **Full-text Search** - Powerful search capabilities built-in
- 📊 **Analytics** - Track usage and engagement (optional)
- 🔐 **Authentication** - Secure access to sensitive information (optional)
- 💬 **Comments** - Allow team members to provide feedback (optional)
- 👥 **Multi-user** - Collaborative editing and workflows
- 📱 **Responsive Design** - Works on desktop, tablet, and mobile
- 🎨 **Customizable** - Easily adapt to your organization's branding

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Git

### Installation

1. Install cookiecutter if you don't have it already:

```bash
pip install cookiecutter
```

2. Generate a new knowledge base project:

```bash
cookiecutter gh:{{ cookiecutter.author_name|lower|replace(" ", "-") }}/{{ cookiecutter.project_slug }}
```

3. Answer the prompts to customize your knowledge base.

4. Navigate to your new project:

```bash
cd your-knowledge-base-name
```

5. Install the requirements:

```bash
pip install -r requirements.txt
```

6. Start the development server:

```bash
mkdocs serve
```

7. Visit [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

---

## 📋 Detailed Usage Guide

### Directory Structure

```
your-knowledge-base/
├── docs/                  # Documentation content
│   ├── assets/            # Images, CSS, and JS files
│   ├── user-guide/        # User guides and documentation
│   └── index.md           # Home page
├── scripts/               # Automation scripts
│   ├── auto_commit.py     # Git automation
│   ├── watch_changes.py   # File watcher
│   └── ...                # Other utilities
├── hooks.py               # Markdown processing hooks
├── mkdocs.yml             # MkDocs configuration
└── requirements.txt       # Python dependencies
```

### Creating Content

1. **Add new articles**

   Create markdown files in the `docs/` directory:

   ```markdown
   # Article Title

   This is the content of my article.

   ## Subheading

   More detailed information here.

   {{category: Development}}
   ```

2. **Update the navigation**

   Edit `mkdocs.yml` to include your new content in the navigation:

   ```yaml
   nav:
     - Home: index.md
     - Getting Started: getting-started.md
     - Your New Article: path/to/article.md
   ```

3. **Use tags and categories**

   Add tags in the front matter:

   ```markdown
   ---
   tags:
     - development
     - guide
   ---

   # Article Title
   ```

   Add categories inline:

   ```markdown
   {{category: Development}}
   ```

### Customization

#### Changing the Theme

Edit `mkdocs.yml` to customize the theme:

```yaml
theme:
  name: material
  palette:
    primary: indigo
    accent: indigo
  features:
    - navigation.tabs
    - navigation.sections
```

#### Adding Extensions

```yaml
markdown_extensions:
  - admonition
  - codehilite
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format
```

---

## 🔧 Configuration Options

When running the cookiecutter template, you'll be prompted for various configuration options:

| Option | Description |
|--------|-------------|
| `project_name` | Name of your knowledge base |
| `project_slug` | URL-friendly version of the name |
| `project_description` | Brief description of your knowledge base |
| `author_name` | Your name or organization |
| `author_email` | Contact email |
| `company_name` | Company or organization name |
| `version` | Initial version number |
| `use_analytics` | Enable usage analytics |
| `use_authentication` | Enable user authentication |
| `use_comments` | Enable commenting features |
| `auto_commit_enabled` | Enable automatic Git commits |
| `file_watcher_enabled` | Enable file change monitoring |
| `open_source_license` | License for your project |

---

## 🔄 Automation Features

### Auto Commit

Automatically commits changes to your Git repository when files are modified:

```bash
python scripts/auto_commit.py
```

Configure in `scripts/auto_commit.py`:

```python
# Configuration options
COMMIT_INTERVAL = 300  # 5 minutes
COMMIT_MESSAGE = "Auto-update: {files}"
```

### File Watcher

Monitors file changes and triggers actions:

```bash
python scripts/watch_changes.py
```

Configure in `scripts/watch_changes.py`:

```python
# Configuration options
WATCH_DIRECTORIES = ["docs"]
IGNORE_PATTERNS = ["*.tmp", "*.bak", "*~"]
```

---

## 🧩 Integrations

### Analytics Integration

If you enabled analytics during setup:

1. Edit `mkdocs.yml`:

```yaml
plugins:
  - analytics:
      provider: google
      property: G-XXXXXXXXXX
```

2. Replace `G-XXXXXXXXXX` with your Google Analytics tracking ID.

### Authentication Integration

If you enabled authentication during setup:

1. Configure authentication providers in `scripts/auth_integration.py`.
2. Set up authentication endpoints:

```python
# Configure authentication providers
AUTH_PROVIDERS = {
    "github": {
        "client_id": "your-client-id",
        "client_secret": "your-client-secret"
    }
}
```

### Comments Integration

If you enabled comments during setup:

1. Configure the comments system in `scripts/comments_integration.py`.
2. Add the comments component to your template.

---

## 🔍 Advanced Usage

### Custom Hooks

Create custom processing hooks by editing `hooks.py`:

```python
def on_file_change(file_path):
    """Hook called when a file changes."""
    print(f"File changed: {file_path}")
    # Add your custom processing here
    return True
```

### Extending with Plugins

Add custom plugins by creating new scripts in the `scripts/` directory:

```python
# scripts/my_plugin.py
def initialize():
    """Initialize the plugin."""
    print("Initializing my plugin")

def process_content(content):
    """Process content."""
    return content.replace("{{placeholder}}", "My Custom Content")
```

---

## 🔌 Plugin Development

1. Create a new Python file in the `scripts/` directory:

```python
# scripts/my_plugin.py
class MyPlugin:
    """Custom plugin for the knowledge base."""
    
    def __init__(self, config=None):
        self.config = config or {}
        
    def on_init(self):
        """Called when the plugin is initialized."""
        print("Plugin initialized!")
        
    def process_markdown(self, markdown):
        """Process markdown content."""
        return markdown.replace("{{mytoken}}", self.config.get("replacement", ""))
```

2. Register your plugin in `scripts/kb_admin.py`:

```python
from scripts.my_plugin import MyPlugin

def register_plugins():
    """Register custom plugins."""
    plugins = {
        "my_plugin": MyPlugin(config={"replacement": "Custom Text"})
    }
    return plugins
```

---

## 🛠 Troubleshooting

### Common Issues

#### MkDocs Build Fails

```
Error: Config value: 'theme'. Error: Unrecognised theme 'material'
```

**Solution**: Install the Material for MkDocs theme:

```bash
pip install mkdocs-material
```

#### File Watcher Not Working

**Solution**: Check permissions and install required dependency:

```bash
pip install watchdog
```

### Getting Help

- Check the [FAQ section](https://example.com/faq)
- Join our [Discord community](https://discord.gg/your-invite)
- Open an [issue on GitHub](https://github.com/{{ cookiecutter.author_name|lower|replace(" ", "-") }}/{{ cookiecutter.project_slug }}/issues)

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

---

## 📄 License

This project is licensed under the {{ cookiecutter.open_source_license }} - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [MkDocs](https://www.mkdocs.org/) for the documentation framework
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) for the beautiful theme
- [Cookiecutter](https://cookiecutter.readthedocs.io/) for the project templating
- All our [contributors](https://github.com/{{ cookiecutter.author_name|lower|replace(" ", "-") }}/{{ cookiecutter.project_slug }}/graphs/contributors) who have helped improve this project

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/{{ cookiecutter.author_name|lower|replace(" ", "-") }}">{{ cookiecutter.author_name }}</a>
</p>
