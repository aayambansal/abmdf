# Installation Guide

## Prerequisites

- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

## Basic Installation

1. Create and activate a virtual environment (recommended):
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Unix or MacOS:
source venv/bin/activate
```

2. Install from PyPI:
```bash
pip install abdmf
```

## Development Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/abdmf.git
cd abdmf
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

3. Install development dependencies:
```bash
pip install -r requirements.txt
pip install -e .
```

## Verification

Verify the installation by running:
```bash
python -c "import abdmf; print(abdmf.__version__)"
```

## Configuration

1. Copy the example configuration:
```bash
cp config/config.yaml.example config/config.yaml
```

2. Edit the configuration file according to your needs:
```bash
# Edit config.yaml with your preferred text editor
vim config/config.yaml
```

## Running Tests

Run the test suite to ensure everything is working:
```bash
pytest tests/
```

## Common Issues

### Missing Dependencies
If you encounter missing dependencies, try:
```bash
pip install --upgrade -r requirements.txt
```

### Permission Issues
If you encounter permission issues during installation:
```bash
pip install --user abdmf
```

### Import Errors
If you get import errors, ensure your Python path includes the installation directory:
```bash
export PYTHONPATH="${PYTHONPATH}:/path/to/abdmf"
```

## Next Steps

After installation, check out the [Usage Guide](usage.md) for examples and best practices.
