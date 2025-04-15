# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build & Run Commands
- Run standard interface: `./run.sh` or `python main.py`
- Run cyberpunk interface: `./run_cyberpunk.sh` or `python cyberpunk_app.py`
- Setup Docker environment: `./setup.sh`
- Docker compose: `docker-compose up -d fuinjutsu-standard` or `docker-compose up -d fuinjutsu-cyberpunk`
- Install dependencies: `pip install -r requirements.txt`

## Code Style Guidelines
- **Imports**: Group imports by stdlib, third-party, then local modules with a blank line between groups
- **Typing**: Use type hints for function parameters and return values
- **Docstrings**: Use Google style docstrings for functions with Args/Returns sections
- **Naming**: Use snake_case for variables/functions and PascalCase for classes
- **Error Handling**: Use try/except blocks with specific exceptions and meaningful error messages
- **Function Structure**: Keep functions focused on a single responsibility
- **Variables**: Use environment variables for API keys and configuration
- **Comments**: Include descriptive comments for complex logic
- **UI Style**: Maintain consistent styling between components
- **API Interactions**: Handle API responses with proper error checking