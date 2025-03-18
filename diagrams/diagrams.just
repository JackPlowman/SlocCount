# ------------------------------------------------------------------------------
# Common Commands
# ------------------------------------------------------------------------------

# Install python dependencies
install:
    uv sync --all-extras

# Create the C4 diagram
create-c4-diagram:
    uv run python c4.py

# ------------------------------------------------------------------------------
# Ruff - Python Linting and Formatting
# Set up ruff red-knot when it's ready
# ------------------------------------------------------------------------------

# Fix all Ruff issues
ruff-fix:
    just diagrams::ruff-format-fix
    just diagrams::ruff-lint-fix

# Check for all Ruff issues
ruff-checks:
    just diagrams::ruff-format-check
    just diagrams::ruff-lint-check

# Check for Ruff issues
ruff-lint-check:
    uv run ruff check .

# Fix Ruff lint issues
ruff-lint-fix:
    uv run ruff check . --fix

# Check for Ruff format issues
ruff-format-check:
    uv run ruff format --check .

# Fix Ruff format issues
ruff-format-fix:
    uv run ruff format .

# ------------------------------------------------------------------------------
# UV
# ------------------------------------------------------------------------------

uv-lock-check:
    uv lock --check
