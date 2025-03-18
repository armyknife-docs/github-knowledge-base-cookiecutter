# GitHub Knowledge Base Makefile
# This Makefile provides commands for managing your GitHub Knowledge Base

# Default Python interpreter
PYTHON := python
# MkDocs binary
MKDOCS := mkdocs

# Help command - lists all available commands
.PHONY: help
help:
	@echo "GitHub Knowledge Base Management Commands"
	@echo "=========================================="
	@echo ""
	@echo "Development Commands:"
	@echo "  make install         - Install dependencies"
	@echo "  make serve           - Start the development server"
	@echo "  make build           - Build the documentation site"
	@echo "  make watch           - Start file watcher for auto-commits"
	@echo "  make hooks           - Set up Git hooks"
	@echo ""
	@echo "Content Management:"
	@echo "  make create-doc      - Create a new document (specify TITLE=\"Title\" [DESC=\"Description\"] [CATEGORY=\"Category\"] [TAGS=\"tag1,tag2\"])"
	@echo "  make generate-tags   - Generate tag pages"
	@echo "  make generate-cats   - Generate category pages"
	@echo ""
	@echo "Deployment:"
	@echo "  make deploy          - Deploy to GitHub Pages"
	@echo ""
	@echo "Advanced Features:"
	@echo "  make setup-comments  - Set up comments system (specify SYSTEM=\"system\" CONFIG=\"path/to/config.json\")"
	@echo "  make setup-analytics - Set up analytics (specify SYSTEM=\"system\" CONFIG=\"path/to/config.json\")"
	@echo "  make setup-auth      - Set up authentication (specify TYPE=\"type\" [CONFIG=\"path/to/config.json\"] [USERS=\"user1:pass1 user2:pass2\"])"
	@echo ""
	@echo "Backup and Maintenance:"
	@echo "  make backup          - Create a backup (specify OUTPUT=\"path/to/backup\" (optional))"
	@echo "  make clean           - Clean build artifacts"
	@echo ""
	@echo "Utility Commands:"
	@echo "  make lint            - Run markdown linter"
	@echo "  make fix-lint        - Attempt to fix common linting issues"

# Installation
.PHONY: install
install:
	@echo "Installing dependencies..."
	$(PYTHON) -m pip install -r requirements.txt
	@echo "Dependencies installed successfully."

# Development server
.PHONY: serve
serve:
	@echo "Starting development server..."
	$(MKDOCS) serve

# Build site
.PHONY: build
build:
	@echo "Building documentation site..."
	$(MKDOCS) build

# Deploy to GitHub Pages
.PHONY: deploy
deploy:
	@echo "Deploying to GitHub Pages..."
	$(MKDOCS) gh-deploy

# Set up Git hooks
.PHONY: hooks
hooks:
	@echo "Setting up Git hooks..."
	$(PYTHON) scripts/setup_hooks.py

# Start file watcher for auto-commits
.PHONY: watch
watch:
	@echo "Starting file watcher for auto-commits..."
	$(PYTHON) scripts/watch_changes.py

# Create a new document
.PHONY: create-doc
create-doc:
	@if [ -z "$(TITLE)" ]; then \
		echo "Error: TITLE is required. Usage: make create-doc TITLE=\"Document Title\" [DESC=\"Description\"] [CATEGORY=\"Category\"] [TAGS=\"tag1,tag2\"]"; \
		exit 1; \
	fi
	@echo "Creating new document: $(TITLE)"
	@CMD="$(PYTHON) scripts/create_document.py \"$(TITLE)\""; \
	if [ ! -z "$(DESC)" ]; then \
		CMD="$$CMD --desc \"$(DESC)\""; \
	fi; \
	if [ ! -z "$(CATEGORY)" ]; then \
		CMD="$$CMD --category \"$(CATEGORY)\""; \
	fi; \
	if [ ! -z "$(TAGS)" ]; then \
		CMD="$$CMD --tags \"$(TAGS)\""; \
	fi; \
	eval $$CMD

# Generate tag pages
.PHONY: generate-tags
generate-tags:
	@echo "Generating tag pages..."
	$(PYTHON) scripts/kb_admin.py generate-tags

# Generate category pages
.PHONY: generate-cats
generate-cats:
	@echo "Generating category pages..."
	$(PYTHON) scripts/generate_categories.py

# Set up comments system
.PHONY: setup-comments
setup-comments:
	@if [ -z "$(SYSTEM)" ] || [ -z "$(CONFIG)" ]; then \
		echo "Error: SYSTEM and CONFIG are required. Usage: make setup-comments SYSTEM=\"disqus|utterances|giscus|isso\" CONFIG=\"path/to/config.json\""; \
		exit 1; \
	fi
	@echo "Setting up $(SYSTEM) comments..."
	$(PYTHON) scripts/comments_integration.py --system $(SYSTEM) --config $(CONFIG)

# Set up analytics
.PHONY: setup-analytics
setup-analytics:
	@if [ -z "$(SYSTEM)" ] || [ -z "$(CONFIG)" ]; then \
		echo "Error: SYSTEM and CONFIG are required. Usage: make setup-analytics SYSTEM=\"google-analytics|plausible|matomo|fathom|umami\" CONFIG=\"path/to/config.json\""; \
		exit 1; \
	fi
	@echo "Setting up $(SYSTEM) analytics..."
	$(PYTHON) scripts/analytics_integration.py --system $(SYSTEM) --config $(CONFIG)

# Set up authentication
.PHONY: setup-auth
setup-auth:
	@if [ -z "$(TYPE)" ]; then \
		echo "Error: TYPE is required. Usage: make setup-auth TYPE=\"nginx|htaccess|oauth2-proxy|keycloak\" [CONFIG=\"path/to/config.json\"] [USERS=\"user1:pass1 user2:pass2\"]"; \
		exit 1; \
	fi
	@echo "Setting up $(TYPE) authentication..."
	@CMD="$(PYTHON) scripts/auth_integration.py --type $(TYPE)"; \
	if [ ! -z "$(CONFIG)" ]; then \
		CMD="$$CMD --config $(CONFIG)"; \
	fi; \
	if [ ! -z "$(USERS)" ]; then \
		CMD="$$CMD --users $(USERS)"; \
	fi; \
	eval $$CMD

# Create a backup
.PHONY: backup
backup:
	@echo "Creating backup..."
	@CMD="$(PYTHON) scripts/kb_admin.py backup"; \
	if [ ! -z "$(OUTPUT)" ]; then \
		CMD="$$CMD --output $(OUTPUT)"; \
	fi; \
	eval $$CMD

# Run markdown linter
.PHONY: lint
lint:
	@echo "Running markdown linter..."
	npx markdownlint-cli "**/*.md" --ignore "node_modules/**"

# Attempt to fix common linting issues
.PHONY: fix-lint
fix-lint:
	@echo "Attempting to fix common linting issues..."
	npx markdownlint-cli --fix "**/*.md" --ignore "node_modules/**"

# Clean build artifacts
.PHONY: clean
clean:
	@echo "Cleaning build artifacts..."
	rm -rf site/
	find . -name "__pycache__" -type d -exec rm -rf {} +
	find . -name "*.pyc" -delete
	@echo "Build artifacts cleaned."

# Default target
.DEFAULT_GOAL := help
