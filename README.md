# Homework Packet Generator

A production-ready Python command-line tool that generates printable homework packets as PDFs using AI. Transform simple topic descriptions into professional, multi-page homework assignments with beautiful formatting.

## ✨ Features

- 🎯 **AI-Powered Content** - Generate assignments using OpenAI GPT models
- 📄 **Professional PDFs** - Beautiful, print-ready homework packets
- 🎨 **Smart Formatting** - HTML/CSS-based layouts with custom styling
- 🧠 **Subject Detection** - Automatic subject classification (Math, Science, English, History)
- 📊 **Difficulty Scaling** - Adjustable complexity and question counts
- 💾 **Cost-Effective** - Local caching reduces API costs during development
- 🔧 **Extensible** - Easy to add new subjects, templates, and styling
- 🎪 **Rich CLI** - Beautiful terminal interface with progress bars

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd homework-gen

# Install with pip (recommended)
pip install -e .

# Or install dependencies manually
pip install -r requirements.txt
```

### Configuration

1. **Set up your OpenAI API key:**
```bash
export OPENAI_API_KEY="your-api-key-here"
```

2. **Configure the application (optional):**
```bash
# Copy the example configuration
cp config.example.yaml config.yaml

# Edit with your preferences
vim config.yaml
```

**⚠️ Security Note:** Never commit real API keys to version control. Use environment variables or local config files.

### Basic Usage

```bash
# Generate math homework
homework-gen "fractions for 5th grade" --count 3 --difficulty medium

# Custom options
homework-gen "photosynthesis" \
  --count 5 \
  --difficulty hard \
  --grade-level "7th Grade" \
  --output biology_homework.pdf \
  --verbose

# See all options
homework-gen --help
```

## 📋 Examples

### Generated Content Preview

```markdown
# Fraction Practice

**Grade Level:** 5th Grade  
**Subject:** Mathematics  
**Difficulty:** Medium  
**Estimated Time:** 20 minutes  

## Learning Objectives
- Add fractions with different denominators
- Simplify fractions to lowest terms
- Convert fractions to decimals

## Problems
1. What is 1/2 + 1/4? (Show your work)
2. Simplify the fraction 8/12
3. Convert 3/4 to a decimal
4. Which is larger: 2/3 or 3/5?
```

### Sample CLI Output

```
📚 Generating 3 medium assignments on: fractions for 5th grade
Using model: gpt-3.5-turbo
Grade level: 5th Grade

Creating assignment requests...  ████████████████████████████████████ 100%
Generating assignment content... ████████████████████████████████████ 100%
Formatting assignments...        ████████████████████████████████████ 100%
Generating PDF...               ████████████████████████████████████ 100%

✓ Generated 3 assignments in PDF: homework_packet_fractions_20250623_181121.pdf
📄 File size: 16,378 bytes
```

## 🏗️ Architecture

### Core Components

The system follows a clean, modular architecture leveraging proven external libraries:

```
homework_generator/
├── cli.py              # Rich CLI interface with Click
├── models.py           # Pydantic data models  
├── config.py           # Configuration management
├── llm_client.py       # OpenAI integration with caching
├── content_generator.py # Assignment generation logic
├── prompt_templates.py # Jinja2 template system
├── formatter.py        # HTML/CSS formatting
└── pdf_generator.py    # WeasyPrint PDF generation
```

### External Libraries

**Why we chose best-in-class libraries instead of custom implementations:**

| Component | Library | Why |
|-----------|---------|-----|
| **CLI** | `click` + `rich` | Industry standard CLI framework with beautiful output |
| **AI Integration** | `litellm` + `openai` | Unified interface for 100+ LLM providers |
| **PDF Generation** | `weasyprint` | CSS-based PDFs with professional typography |
| **Data Validation** | `pydantic` | Type-safe models with automatic validation |
| **Templates** | `jinja2` | Flexible, secure template engine |
| **Testing** | `pytest` | De facto standard for Python testing |
| **Caching** | `diskcache` | Persistent, thread-safe caching |

This approach ensures:
- 🛡️ **Reliability** - Battle-tested libraries with millions of users
- 🚀 **Performance** - Optimized implementations
- 📖 **Maintainability** - Standard APIs and documentation
- 🔧 **Extensibility** - Easy to add features and integrations

## 🧪 Testing & Development

### Run Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test modules
pytest tests/test_models.py tests/test_cli.py -v

# Run with coverage
pytest tests/ --cov=homework_generator --cov-report=html
```

### Try the Demo

```bash
# See the system in action
python demo.py

# Run integration tests
python test_integration.py
```

### Code Quality

```bash
# Format code
black homework_generator/ tests/

# Type checking
mypy homework_generator/

# Linting
flake8 homework_generator/
```

## 📁 Project Structure

```
homework-gen/
├── homework_generator/         # Main package
│   ├── __init__.py
│   ├── cli.py                 # Command-line interface
│   ├── models.py              # Data models
│   ├── config.py              # Configuration
│   ├── llm_client.py          # LLM integration
│   ├── content_generator.py   # Assignment generation
│   ├── prompt_templates.py    # Template system
│   ├── formatter.py           # HTML/CSS formatting
│   └── pdf_generator.py       # PDF generation
├── templates/                  # Templates and styling
│   ├── prompts/               # LLM prompt templates
│   │   ├── math.md
│   │   ├── science.md
│   │   └── generic.md
│   ├── assignment.html        # HTML template
│   └── styles.css             # PDF styling
├── tests/                     # Test suite
├── config.yaml               # Configuration file
├── requirements.txt          # Dependencies
├── requirements-dev.txt      # Development dependencies
├── pyproject.toml           # Project metadata
├── demo.py                  # Demo script
└── README.md               # This file
```

## ⚙️ Configuration

The system uses a hierarchical configuration approach:

1. **Environment Variables** (highest priority)
2. **config.yaml file**
3. **Default values** (lowest priority)

### Configuration Options

```yaml
llm:
  api_key: "${OPENAI_API_KEY}"    # OpenAI API key
  model: "gpt-3.5-turbo"          # Model to use
  base_url: null                  # Custom API endpoint

generation:
  default_count: 5                # Default number of assignments
  default_difficulty: "medium"    # Default difficulty level
  default_grade_level: "5th Grade" # Default grade level

pdf:
  default_theme: "classroom"      # PDF styling theme
  include_answer_key: false       # Include answer keys (future)

cache:
  enabled: true                   # Enable LLM response caching
  directory: "llm_cache"          # Cache directory
```

## 🔧 Extending the System

### Adding New Subjects

1. Create a prompt template in `templates/prompts/`:
```markdown
# templates/prompts/chemistry.md
Generate chemistry assignments for {{grade_level}} students on {{topic}}.

Include:
- Lab safety reminders
- Chemical equations
- Real-world applications
```

2. The system automatically detects and uses new templates.

### Custom PDF Styling

1. Edit `templates/styles.css` for global styling
2. Modify `templates/assignment.html` for layout changes
3. Both support full HTML/CSS features

### Adding New LLM Providers

The system uses `litellm` which supports 100+ providers out of the box:

```python
# Just change the model name
llm_client = LLMClient(model="claude-3-sonnet")  # Anthropic
llm_client = LLMClient(model="ollama/llama2")    # Local via Ollama
```

## 🛠️ Development

### Setting Up Development Environment

```bash
# Clone and setup
git clone <repository-url>
cd homework-gen
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install in development mode
pip install -e .
pip install -r requirements-dev.txt

# Run tests
pytest
```

### Contributing

1. **Code Style**: Use `black` for formatting, `mypy` for type checking
2. **Tests**: Add tests for new features in `tests/`
3. **Documentation**: Update README and docstrings
4. **Templates**: Test new prompt templates thoroughly

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **OpenAI** - For the GPT models that power content generation
- **WeasyPrint** - For excellent HTML-to-PDF conversion
- **Click** - For the beautiful CLI framework
- **Rich** - For terminal styling and progress bars
- **Pydantic** - For data validation and configuration management

---

**Made with ❤️ for educators, parents, and students everywhere.**
```
SYSTEM: You are an expert educator creating homework assignments.

[TEMPLATE CONTENT FROM .md FILE - RENDERED WITH USER PARAMETERS]

OUTPUT FORMAT:
You must respond with valid JSON containing an array of assignments.
Each assignment must follow this exact structure:

{json_schema}

EXAMPLES:
{few_shot_examples_from_json_file}

USER REQUEST: {user_description}

Remember: Respond ONLY with valid JSON. No additional text or explanations.
```

### Template Files

Templates are stored as Markdown files in `templates/prompts/` and loaded dynamically:

**Math Template** (`templates/prompts/math.md`):
```markdown
# Mathematics Assignment Generation

You are creating {count} mathematics assignments for {grade_level} students on the topic: **{topic}**

## Focus Areas
- Clear, step-by-step problems
- Age-appropriate complexity  
- Practical applications when possible
- Variety in problem types

## Difficulty Guidelines
- **Easy**: Basic recall and simple applications
- **Medium**: Multi-step problems requiring reasoning  
- **Hard**: Complex problems requiring multiple concepts

**Target Difficulty**: {difficulty}

## Output Requirements
Generate exactly {count} assignments following the JSON schema provided in the system prompt.
```

**Reading Comprehension Template** (`templates/prompts/reading.md`):
```markdown  
# Reading Comprehension Assignment Generation

Create {count} reading comprehension assignments for {grade_level} students on: **{topic}**

## Requirements
- Age-appropriate reading passages (200-500 words for elementary, 500-800 for middle school)
- Comprehension questions of varying types:
  * Literal understanding (who, what, when, where)
  * Inferential reasoning (why, how, implications)
  * Critical thinking (analysis, evaluation, connections)
- Vocabulary exercises related to the passage

## Difficulty Level: {difficulty}
- **Easy**: Simple passages with basic comprehension questions
- **Medium**: More complex passages with inferential questions
- **Hard**: Advanced passages requiring critical analysis

## Content Guidelines
- Ensure passages are engaging and age-appropriate
- Include diverse topics and perspectives
- Avoid controversial or sensitive subjects unless specifically requested
```

### Output Validation

The system includes robust parsing and validation:

1. **JSON Schema Validation**: Ensures LLM output matches expected structure
2. **Content Sanitization**: Removes potentially problematic formatting
3. **Fallback Handling**: Retry with simplified prompts if parsing fails
4. **Quality Checks**: Validates assignment coherence and appropriateness

### Error Handling

- **Malformed JSON**: Attempt to extract assignments using regex patterns
- **Missing Fields**: Provide sensible defaults for optional fields
- **Content Issues**: Flag inappropriate content and regenerate
- **Model Failures**: Graceful degradation to simpler models or manual templates

## Workflow

1. **Command Line Input**
   ```bash
   python -m homework_generator "Algebra practice for 7th grade" --count 5 --difficulty medium
   ```

2. **Template Selection & Prompt Generation**
   - Load appropriate template from `templates/prompts/{subject}.md` (user specifies or defaults to generic)
   - Render template with user parameters using Jinja2
   - Load few-shot examples from `templates/examples/{subject}.json`
   - Combine into final structured prompt

3. **LLM Query**
   - Send structured prompt to configured LLM (local or remote)
   - Parse JSON response into Assignment objects
   - Validate against schema and retry if malformed

4. **Content Processing**
   - Convert Assignment objects to standardized Markdown
   - Apply consistent formatting and styling
   - Add metadata headers and page break markers

5. **PDF Generation**
   - Convert Markdown to HTML with CSS styling
   - Generate PDF with one assignment per page
   - Include header/footer with assignment numbers

6. **Output**
   - Save PDF to specified location
   - Provide summary of generated assignments

## Command Line Interface

```bash
# Basic usage
homework-gen "Fractions for 5th grade"

# Advanced options
homework-gen "Reading comprehension on space exploration" \
  --count 10 \
  --difficulty hard \
  --grade-level 8 \
  --output space_homework.pdf \
  --model gpt-4 \
  --template reading \
  --theme classroom

# Use local model
homework-gen "Basic arithmetic" --model ollama/llama2 --template math
```

## Configuration

The tool supports configuration via:
- Command line arguments (highest priority)
- Environment variables
- `config.yaml` file in project directory (copy from `config.example.yaml`)
- Default values

**⚠️ Security:** Use environment variables for sensitive data like API keys.

Example `config.yaml`:
```yaml
llm:
  default_model: "gpt-4"
  api_key: "your-openai-api-key-here"  # Set via OPENAI_API_KEY env var
  local_models:
    - "ollama/llama2"
    - "ollama/mistral"

pdf:
  theme: "classroom"
  font_family: "Arial"
  page_size: "letter"

generation:
  default_count: 5
  default_difficulty: "medium"
```

## Testing Strategy

### Unit Tests
- **LLM Client**: Mock API responses, test error handling
- **Content Generator**: Validate prompt generation and response parsing
- **Formatter**: Test Markdown processing and edge cases
- **PDF Generator**: Verify PDF structure without visual checks
- **CLI**: Test argument parsing and command execution

### Integration Tests
- **End-to-End**: Generate actual homework packets with mock LLM
- **Local Model**: Test with actual Ollama integration
- **File I/O**: Verify PDF creation and file handling

### Test Data
- Sample LLM responses for different subjects (`tests/fixtures/sample_llm_responses.json`)
- Expected Markdown outputs (`tests/fixtures/expected_assignments.json`)  
- Template rendering tests (`tests/fixtures/test_prompts.json`)
- Mock template files for testing (`tests/fixtures/templates/`)

## Project Structure

```
homework-gen/
├── homework_generator/
│   ├── __init__.py
│   ├── cli.py
│   ├── llm_client.py
│   ├── content_generator.py
│   ├── prompt_templates.py
│   ├── formatter.py
│   ├── pdf_generator.py
│   ├── config.py
│   └── models.py
├── tests/
│   ├── __init__.py
│   ├── test_cli.py
│   ├── test_llm_client.py
│   ├── test_content_generator.py
│   ├── test_prompt_templates.py
│   ├── test_formatter.py
│   ├── test_pdf_generator.py
│   └── fixtures/
│       ├── sample_llm_responses.json
│       ├── expected_assignments.json
│       └── test_prompts.json
├── templates/
│   ├── assignment.html
│   ├── styles.css
│   ├── prompts/
│   │   ├── math.md
│   │   ├── reading.md
│   │   ├── science.md
│   │   ├── history.md
│   │   ├── writing.md
│   │   └── generic.md
│   └── examples/
│       ├── math.json
│       ├── reading.json
│       ├── science.json
│       ├── history.json
│       └── writing.json
├── config.yaml
├── requirements.txt
├── requirements-dev.txt
├── pyproject.toml
├── .gitignore
└── README.md
```

## Installation

```bash
# Clone repository
git clone <repo-url>
cd homework-gen

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

## Development

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Run with coverage
pytest --cov=homework_generator

# Format code
black homework_generator tests
isort homework_generator tests

# Type checking
mypy homework_generator
```

## Examples

### Generated Assignment Structure
Each assignment will be generated as JSON, then converted to this Markdown format:
```markdown
# Assignment 1: Basic Fractions

**Grade Level:** 5th Grade  
**Subject:** Mathematics  
**Difficulty:** Medium  
**Estimated Time:** 15 minutes  
**Materials Needed:** Pencil, calculator  

## Learning Objectives
- Students will add and subtract fractions with different denominators
- Students will simplify fractions to lowest terms

## Instructions
Complete the following fraction problems. Show your work for each problem.

## Problems
1. What is 1/2 + 1/4?
2. Simplify 6/8 to its lowest terms.
3. A pizza is cut into 8 slices. If you eat 3 slices, what fraction of the pizza did you eat?
...
```

### JSON Schema for LLM Responses
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "assignments": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "title": {"type": "string"},
          "grade_level": {"type": "string"},
          "subject": {"type": "string"},
          "difficulty": {"type": "string", "enum": ["Easy", "Medium", "Hard"]},
          "estimated_time": {"type": "string"},
          "instructions": {"type": "string"},
          "problems": {"type": "array", "items": {"type": "string"}},
          "materials_needed": {"type": "array", "items": {"type": "string"}},
          "learning_objectives": {"type": "array", "items": {"type": "string"}}
        },
        "required": ["title", "grade_level", "subject", "difficulty", "instructions", "problems"]
      }
    }
  },
  "required": ["assignments"]
}
```

## Future Enhancements

- Web interface for non-technical users
- Integration with learning management systems
- Support for different languages
- Answer key generation
- Progress tracking and analytics
- Collaborative assignment creation

## Contributing

1. Fork the repository
2. Create a feature branch
3. Write tests for new functionality
4. Implement the feature
5. Ensure all tests pass
6. Submit a pull request

## License

MIT License
