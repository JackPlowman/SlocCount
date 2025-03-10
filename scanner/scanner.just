# ------------------------------------------------------------------------------
# Common Commands
# ------------------------------------------------------------------------------

# Install python dependencies
install:
    uv sync --all-extras

# Run the analyser
run:
    uv run python -m main.py

# Run the analyser with default values
run-with-defaults:
    INPUT_DEBUG=true INPUT_REPOSITORY_OWNER=JackPlowman uv run python main.py

# ------------------------------------------------------------------------------
# Test Commands
# ------------------------------------------------------------------------------

# Run unit tests
unit-test:
    uv run pytest . --cov=. --cov-report=xml

# Run unit tests with debug output
unit-test-debug:
    uv run pytest . --cov=. --cov-report=xml -vvvv
