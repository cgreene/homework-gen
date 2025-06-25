# Homework Generator

A production-ready Python CLI tool that generates custom homework assignments as beautiful PDFs using AI. Perfect for teachers, parents, and tutors who need personalized educational content.

## ✨ Features

- 🤖 **AI-Powered Content** - Uses OpenAI GPT models to generate engaging assignments
- 📄 **Professional PDFs** - Beautiful, print-ready homework packets with custom styling
- 🎯 **Flexible Topics** - Works with any subject: math, science, history, language arts, etc.
- 📊 **Customizable Difficulty** - Easy, medium, or hard assignments
- 🎓 **Grade-Specific** - Tailored content for any grade level (K-12)
- 💾 **Smart Caching** - Reduces API costs by caching responses
- 🎨 **Professional Layout** - Clean HTML/CSS templates for consistent formatting
- 🖥️ **Rich CLI** - Beautiful terminal interface with progress bars

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/homework-gen.git
cd homework-gen

# Install the package
pip install -e .
```

### Setup

1. **Get an OpenAI API key** from [OpenAI's website](https://platform.openai.com/api-keys)

2. **Set your API key** (choose one method):
   ```bash
   # Option 1: Environment variable (recommended)
   export OPENAI_API_KEY="your-api-key-here"
   
   # Option 2: Configuration file
   cp config.example.yaml config.yaml
   # Edit config.yaml and add your API key
   ```

3. **Test the installation**:
   ```bash
   homework-gen --help
   ```

### Basic Usage

**⚠️ Important**: You must specify a grade level for all assignments.

```bash
# Generate basic math homework
homework-gen "fractions" --grade-level "5th Grade"

# Generate science homework with custom options
homework-gen "photosynthesis" \
  --grade-level "7th Grade" \
  --count 5 \
  --difficulty hard \
  --output my_homework.pdf

# Generate reading comprehension for elementary
homework-gen "short stories with comprehension questions" \
  --grade-level "3rd Grade" \
  --count 3 \
  --difficulty easy
```

## 📚 Examples

### Command Examples

```bash
# Math for different grades
homework-gen "multiplication tables" --template math --grade-level "3rd Grade" --count 4
homework-gen "quadratic equations" --template math --grade-level "9th Grade" --difficulty hard

# Science topics
homework-gen "solar system" --template science --grade-level "4th Grade" --count 3
homework-gen "chemical reactions" --template science --grade-level "10th Grade" --difficulty medium

# Language arts
homework-gen "creative writing prompts" --template english --grade-level "6th Grade"
homework-gen "grammar exercises" --template english --grade-level "5th Grade" --count 5

# History and social studies
homework-gen "American Revolution" --template social_studies --grade-level "8th Grade" --difficulty medium
homework-gen "community helpers" --template social_studies --grade-level "1st Grade" --count 2

# Computer science and technology
homework-gen "programming basics" --template computer_science --grade-level "7th Grade"
homework-gen "digital citizenship" --template computer_science --grade-level "5th Grade"

# Arts and creative subjects
homework-gen "watercolor painting" --template art --grade-level "4th Grade"
homework-gen "music theory basics" --template music --grade-level "6th Grade"
```

### Sample Generated Content

```markdown
# Fraction Practice Worksheet

**Grade Level:** 5th Grade  
**Subject:** Mathematics  
**Difficulty:** Medium  
**Estimated Time:** 25 minutes  

## Learning Objectives
- Add and subtract fractions with like denominators
- Identify equivalent fractions
- Convert improper fractions to mixed numbers

## Problems

1. Add the fractions: 2/8 + 3/8 = ___

2. Which fraction is equivalent to 1/2?
   a) 2/6  b) 3/6  c) 4/6  d) 5/6

3. Convert to a mixed number: 11/4 = ___

[... more problems ...]

## Answer Key
1. 5/8
2. b) 3/6
3. 2¾
```

### CLI Output

```
📚 Generating 3 medium assignments on: fractions for 5th grade
🤖 Using model: gpt-4o-mini
🎓 Grade level: 5th Grade

Creating assignment requests...  ████████████████████████████████████ 100%
Generating assignment content... ████████████████████████████████████ 100%
Formatting assignments...        ████████████████████████████████████ 100%
Generating PDF...               ████████████████████████████████████ 100%

✅ Generated homework packet: homework_packet_fractions_for_5th_grade_20250623_185803.pdf
📄 File size: 847 KB | 3 assignments | 12 pages
```

## 🛠️ Command Line Options

```bash
homework-gen [TOPIC] [OPTIONS]

Required:
  TOPIC                Topic for the homework (e.g., "fractions", "photosynthesis")
                      Optional when using --list-templates

Required Options:
  --grade-level TEXT   Grade level (e.g., "5th Grade", "High School")

Optional:
  --count INTEGER      Number of assignments (default: 5)
  --difficulty TEXT    Difficulty level: easy, medium, hard (default: medium)
  --template TEXT      Subject-specific template (default: generic)
                      Use --list-templates to see all available options
  --output TEXT        Output PDF filename (auto-generated if not specified)
  --verbose           Show detailed progress information
  --list-templates    Show all available prompt templates
  --help              Show this help message
```

### 🎨 Using Subject-Specific Templates

The system includes specialized templates for different subjects. Use the `--template` flag to get better, more focused results:

```bash
# List all available templates
homework-gen --list-templates

# Use specific templates for better results
homework-gen "algebra equations" --template math --grade-level "8th Grade"
homework-gen "photosynthesis" --template science --grade-level "7th Grade" 
homework-gen "creative writing" --template english --grade-level "6th Grade"
homework-gen "American Revolution" --template social_studies --grade-level "8th Grade"
homework-gen "programming loops" --template computer_science --grade-level "9th Grade"
homework-gen "watercolor techniques" --template art --grade-level "5th Grade"
```

Available templates include:
- `math` - Mathematics and arithmetic
- `science` - General science topics
- `english` - Language arts, writing, literature
- `social_studies` - History, geography, civics
- `computer_science` - Programming, algorithms, digital citizenship
- `art` - Visual arts, art history, techniques
- `music` - Music theory, performance, composition
- `health` - Personal health, nutrition, safety
- `physical_education` - Fitness, sports, movement
- `world_languages` - Foreign language learning
- `psychology` - Human behavior, mental health
- `economics` - Economic systems, personal finance
- `philosophy` - Critical thinking, ethics, logic
- `environmental_science` - Ecology, sustainability
- `career_technical` - Vocational skills, workplace readiness
- `generic` - Fallback for any topic

## ⚙️ Configuration

The tool supports configuration via:
1. Environment variables (highest priority)
2. `config.yaml` file
3. Built-in defaults (lowest priority)

### Configuration File

Copy `config.example.yaml` to `config.yaml` and customize:

```yaml
llm:
  default_model: "gpt-4o-mini"        # OpenAI model to use
  api_key: "${OPENAI_API_KEY}"        # Your API key (use env var)
  base_url: null                      # Custom API endpoint (optional)

generation:
  default_count: 5                    # Default number of assignments
  default_difficulty: "medium"        # Default difficulty level

pdf:
  theme: "classroom"                  # PDF styling theme
  font_family: "Arial"               # Font for PDFs
  page_size: "letter"                # Page size (letter, a4, etc.)
```

**🔒 Security Note**: Never commit your real API key to version control. Use environment variables or keep `config.yaml` local.

## 🏗️ Project Structure

```
homework-gen/
├── homework_generator/         # Main Python package
│   ├── cli.py                 # Command-line interface
│   ├── models.py              # Data models and validation
│   ├── config.py              # Configuration management
│   ├── llm_client.py          # OpenAI API integration
│   ├── content_generator.py   # Assignment generation logic
│   ├── prompt_templates.py    # AI prompt management
│   ├── formatter.py           # HTML formatting
│   └── pdf_generator.py       # PDF creation
├── templates/                  # HTML/CSS templates
│   ├── assignment.html        # Main assignment template
│   ├── styles.css            # PDF styling
│   └── prompts/              # AI prompt templates
│       ├── math.md
│       ├── generic.md
│       └── ...
├── tests/                     # Test suite
├── config.example.yaml       # Example configuration
├── requirements.txt          # Dependencies
└── README.md                # This file
```

## 🧪 Development

### Running Tests

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest

# Run with coverage
pytest --cov=homework_generator

# Run specific test files
pytest tests/test_cli.py -v
```

### Code Quality

```bash
# Format code
black homework_generator/ tests/

# Check formatting
black --check homework_generator/

# Lint code
ruff check homework_generator/
```

### Demo and Integration Tests

```bash
# Try the demo
python demo.py

# Run integration tests
python test_integration.py
```

## 🔧 Extending the System

### Adding Custom Prompts

Create new prompt templates in `templates/prompts/`:

```markdown
<!-- templates/prompts/chemistry.md -->
# Chemistry Assignment Generator

Generate {{count}} chemistry assignments for {{grade_level}} students on: {{topic}}

Requirements:
- Include safety reminders
- Use age-appropriate language
- Add real-world applications
- Difficulty: {{difficulty}}
```

### Customizing PDF Appearance

Edit the templates:
- `templates/assignment.html` - Layout and structure
- `templates/styles.css` - Colors, fonts, spacing

### Adding New Models

The system supports any OpenAI-compatible API:

```yaml
# Use different models
llm:
  default_model: "gpt-4"              # More capable model
  default_model: "gpt-3.5-turbo"     # Faster and cheaper
```

## 📋 Troubleshooting

### Common Issues

**"No API key found"**
```bash
# Make sure your API key is set
echo $OPENAI_API_KEY
export OPENAI_API_KEY="your-key-here"
```

**"Grade level is required"**
```bash
# Always specify grade level
homework-gen "fractions" --grade-level "5th Grade"
```

**"Permission denied" on PDF**
```bash
# Make sure the output directory is writable
homework-gen "math" --grade-level "3rd Grade" --output ~/Desktop/homework.pdf
```

### Getting Help

- Check `homework-gen --help` for all options
- Look at `demo.py` for working examples
- Review the test files in `tests/` for usage patterns

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

Built with excellent open-source tools:
- [OpenAI](https://openai.com/) - GPT models for content generation
- [Click](https://click.palletsprojects.com/) - Command-line interface framework
- [Rich](https://rich.readthedocs.io/) - Beautiful terminal output
- [WeasyPrint](https://weasyprint.org/) - HTML to PDF conversion
- [Pydantic](https://pydantic.dev/) - Data validation and settings

---

**Made with ❤️ for educators everywhere.**
