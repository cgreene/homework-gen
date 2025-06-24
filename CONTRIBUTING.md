# Contributing to Homework Generator

Thank you for your interest in contributing to the Homework Generator! This document provides guidelines for contributing to this project.

## Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd homework-gen
   ```

2. **Set up Python environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements-dev.txt
   pip install -e .
   ```

4. **Run tests to verify setup**
   ```bash
   pytest tests/ -v
   ```

## Project Structure

```
homework-gen/
├── homework_generator/           # Main package
│   ├── cli.py                   # Command-line interface
│   ├── models.py                # Pydantic data models
│   ├── config.py                # Configuration management
│   ├── llm_client.py            # AI integration
│   ├── content_generator.py     # Assignment generation
│   ├── prompt_templates.py      # Template system
│   ├── formatter.py             # HTML/CSS formatting
│   └── pdf_generator.py         # PDF generation
├── templates/                    # Templates and styling
├── tests/                        # Test suite
└── docs/                         # Documentation
```

## Code Standards

### Code Quality
- **Formatting**: Use `black` for code formatting
- **Linting**: Use `ruff` for linting
- **Type Hints**: Add type hints to all functions and methods
- **Documentation**: Write clear docstrings for all public functions

### Running Quality Checks
```bash
# Format code
black homework_generator/ tests/

# Lint code
ruff check homework_generator/ tests/

# Type checking (optional)
mypy homework_generator/
```

### Testing
- Write tests for all new functionality
- Maintain test coverage above 90%
- Use pytest for testing framework
- Mock external dependencies (LLM calls, file system, etc.)

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_models.py -v

# Run with coverage
pytest tests/ --cov=homework_generator --cov-report=html
```

## Making Changes

### Branch Naming
- `feature/description` for new features
- `bugfix/description` for bug fixes
- `docs/description` for documentation updates

### Commit Messages
Use clear, descriptive commit messages:
- `feat: add support for new subject templates`
- `fix: resolve PDF generation error with special characters`
- `docs: update README with new installation instructions`
- `test: add tests for content generator validation`

### Pull Request Process

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clean, well-documented code
   - Add tests for new functionality
   - Update documentation if needed

3. **Test your changes**
   ```bash
   pytest tests/ -v
   black homework_generator/ tests/
   ruff check homework_generator/ tests/
   ```

4. **Submit a pull request**
   - Provide a clear description of changes
   - Reference any related issues
   - Ensure all tests pass

## Adding New Features

### New Subject Templates
To add a new subject template:

1. Create a new template file in `templates/prompts/`
2. Add the subject to the detection logic in `cli.py`
3. Write tests for the new subject
4. Update documentation

### New Output Formats
To add a new output format:

1. Extend the formatter in `formatter.py`
2. Add appropriate templates
3. Update the CLI to support the new format
4. Write comprehensive tests

### New LLM Providers
The project uses LiteLLM which supports 100+ providers. To add support:

1. Update configuration options
2. Add provider-specific handling if needed
3. Test with the new provider
4. Update documentation

## Architecture Guidelines

### Design Principles
- **Separation of Concerns**: Each module has a single responsibility
- **Dependency Injection**: Pass dependencies explicitly
- **Configuration Over Code**: Use configuration for customizable behavior
- **Fail Fast**: Validate inputs early and provide clear error messages

### External Dependencies
- Prefer established, well-maintained libraries
- Minimize dependencies where possible
- Use semantic versioning for dependency constraints
- Document why each dependency is necessary

### Error Handling
- Use custom exceptions for domain-specific errors
- Provide helpful error messages to users
- Log errors appropriately for debugging
- Gracefully handle external service failures

## Testing Guidelines

### Test Organization
- One test file per module (`test_models.py` for `models.py`)
- Group related tests in classes
- Use descriptive test names that explain the scenario

### Test Types
- **Unit Tests**: Test individual functions/methods
- **Integration Tests**: Test component interactions
- **End-to-End Tests**: Test complete workflows

### Mocking
- Mock external services (OpenAI, file system)
- Use `pytest-mock` for mocking
- Verify mock calls to ensure correct integration

## Documentation

### Code Documentation
- Write docstrings for all public functions and classes
- Use Google-style docstrings
- Include examples for complex functions

### User Documentation
- Keep README.md up to date
- Include examples for new features
- Document configuration options

## Getting Help

- Check existing issues for similar problems
- Review the codebase and tests for examples
- Ask questions in pull request comments
- Refer to the comprehensive test suite for usage patterns

## Code of Conduct

- Be respectful and constructive in discussions
- Focus on the code and technical issues
- Help create a welcoming environment for all contributors
- Follow the project's technical standards and guidelines

Thank you for contributing to Homework Generator!
