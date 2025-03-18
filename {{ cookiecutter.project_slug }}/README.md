# {{ cookiecutter.project_name }}

{{ cookiecutter.project_description }}

## Getting Started

1. Install requirements:
   ```
   pip install -r requirements.txt
   ```

2. Start the development server:
   ```
   mkdocs serve
   ```

3. Visit http://127.0.0.1:8000 in your browser

## Features

{% if cookiecutter.use_analytics == "yes" %}
- Analytics integration
{% endif %}
{% if cookiecutter.use_authentication == "yes" %}
- Authentication system
{% endif %}
{% if cookiecutter.use_comments == "yes" %}
- Comments functionality
{% endif %}
{% if cookiecutter.auto_commit_enabled == "yes" %}
- Automatic git commits
{% endif %}
{% if cookiecutter.file_watcher_enabled == "yes" %}
- File change monitoring
{% endif %}

## Author

{{ cookiecutter.author_name }} ({{ cookiecutter.author_email }})
