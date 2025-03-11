# ------------------------------------------------------------------------------
# Common Commands
# ------------------------------------------------------------------------------

# Install python dependencies
install:
    uv sync --all-extras

# Run the analyser
run:
    uv run python -m app

# Run the analyser with default values
run-with-defaults:
    INPUT_DEBUG=true INPUT_REPOSITORY_OWNER=JackPlowman uv run python -m app

# ------------------------------------------------------------------------------
# Test Commands
# ------------------------------------------------------------------------------

# Run unit tests
unit-test:
    uv run pytest app --cov=. --cov-report=xml

# Run unit tests with debug output
unit-test-debug:
    uv run pytest app --cov=. --cov-report=xml -vvvv

# ------------------------------------------------------------------------------
# Ruff - Python Linting and Formatting
# Set up ruff red-knot when it's ready
# ------------------------------------------------------------------------------

# Fix all Ruff issues
ruff-fix:
    just scanner::ruff-format-fix
    just scanner::ruff-lint-fix

# Check for all Ruff issues
ruff-checks:
    just scanner::ruff-format-check
    just scanner::ruff-lint-check

# Check for Ruff issues
ruff-lint-check:
    uv run ruff check app

# Fix Ruff lint issues
ruff-lint-fix:
    uv run ruff check app --fix

# Check for Ruff format issues
ruff-format-check:
    uv run ruff format --check app

# Fix Ruff format issues
ruff-format-fix:
    uv run ruff format app

# ------------------------------------------------------------------------------
# Other Python Tools
# ------------------------------------------------------------------------------

# Check for unused code
vulture:
    uv run vulture app
