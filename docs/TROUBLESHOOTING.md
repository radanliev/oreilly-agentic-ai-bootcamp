# Troubleshooting

## Common Issues

### `ModuleNotFoundError: No module named 'shared'`

Make sure you're running from the repository root and the package is installed:

```bash
cd oreilly-agentic-ai-bootcamp
pip install -e ".[dev]"
```

### `ModuleNotFoundError: No module named 'cryptography'`

Install the cryptography library:

```bash
pip install cryptography>=42.0.0
```

### `ModuleNotFoundError: No module named 'yaml'`

Install PyYAML:

```bash
pip install pyyaml>=6.0
```

### Tests fail with import errors

Run from the repository root directory:

```bash
python3 -m pytest shared/tests/ -v
```

### `pip install -e .` fails with PEP 668 error

On macOS with Homebrew Python:

```bash
pip install -e ".[dev]" --break-system-packages
```

Or use a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### Session demo scripts fail to find shared modules

Ensure you're running from the repository root, not from a session directory:

```bash
# Correct
python3 session-1-blind-verification/run_demo.py

# Wrong (from inside session-1/)
cd session-1 && python3 run_demo.py  # This may fail
```

## Getting Help

- Check the [README](../README.md) for setup instructions
- See [FACILITATOR_GUIDE](FACILITATOR_GUIDE.md) for session-specific help
