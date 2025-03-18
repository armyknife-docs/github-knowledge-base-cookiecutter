# GitHub Knowledge Base Cookiecutter Template

[![GitHub release](https://img.shields.io/github/release/armyknife-docs/github-knowledge-base.svg)](https://github.com/armyknife-docs/github-knowledge-base-cookiecutter/releases)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A flexible, feature-rich cookiecutter template for creating MkDocs-powered GitHub knowledge bases and documentation sites.

## Features

- 🚀 **MkDocs Integration** - Built on the popular static site generator with Material theme
- 🔄 **Git Automation** - Optional scripts for auto-commits and change tracking
- 🏷️ **Tagging System** - Built-in tag and category management
- 📊 **Analytics** - Optional Google Analytics integration
- 🔐 **Authentication** - Optional user authentication support
- 💬 **Comments** - Optional comments functionality for feedback
- 📱 **Responsive Design** - Mobile-friendly interface out of the box
- 🎨 **Customizable** - Easily adapt to your organization's branding
- 🧩 **Extensible** - Plugin system for adding custom functionality

## Requirements

- Python 3.8+
- Cookiecutter 2.1.0+
- Git

## Usage

### Creating a New Knowledge Base

```bash
# Install cookiecutter if you don't have it
pip install cookiecutter

# Generate a new GitHub Knowledge Base project
cookiecutter gh:yourusername/github-knowledge-base
```

### Template Options

When you run the cookiecutter command, you'll be prompted for these values:

| Option | Description | Default |
|--------|-------------|---------|
| `project_name` | Name of your knowledge base | Knowledge Base |
| `project_slug` | URL-friendly version of the name | knowledge-base |
| `project_description` | Brief description | A customizable knowledge base powered by MkDocs |
| `author_name` | Your name or organization | Your Name |
| `author_email` | Contact email | your.email@example.com |
| `company_name` | Company or organization name | Your Company |
| `version` | Initial version number | 0.1.0 |
| `use_analytics` | Enable usage analytics | no |
| `use_authentication` | Enable user authentication | no |
| `use_comments` | Enable commenting features | no |
| `auto_commit_enabled` | Enable automatic Git commits | no |
| `file_watcher_enabled` | Enable file change monitoring | no |
| `open_source_license` | License for your project | MIT |

## Directory Structure

The generated project will have the following structure:

```
your-knowledge-base/
├── docs/                  # Documentation content
│   ├── assets/            # Images, CSS, and JS files
│   ├── user-guide/        # User guides and documentation
│   └── index.md           # Home page
├── scripts/               # Automation scripts
│   ├── auto_commit.py     # Git automation (if enabled)
│   ├── watch_changes.py   # File watcher (if enabled)
│   └── ...                # Other utilities
├── hooks.py               # Markdown processing hooks
├── mkdocs.yml             # MkDocs configuration
└── requirements.txt       # Python dependencies
```

## Example

After generating your project:

```bash
# Navigate to your new project
cd your-knowledge-base

# Install the requirements
pip install -r requirements.txt

# Start the development server
mkdocs serve
```

Visit http://127.0.0.1:8000 in your browser to see your new knowledge base.

## Advanced Usage

### Customizing the Template

If you want to customize this cookiecutter template:

1. Fork the repository
2. Clone your fork
3. Make changes to the template
4. Test your changes with `cookiecutter path/to/your/fork`
5. Submit a pull request

### Adding Your Own Hooks

The template includes a `hooks/post_gen_project.py` script that runs after the project is generated. You can modify this to add your own post-processing steps.

## Demo

![Knowledge Base Demo](demo.gif)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Credits

- [MkDocs](https://www.mkdocs.org/) for the documentation framework
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) for the beautiful theme
- [Cookiecutter](https://cookiecutter.readthedocs.io/) for the project templating

## Support

If you encounter any problems or have any questions, please [open an issue](https://github.com/yourusername/github-knowledge-base/issues) on GitHub.
