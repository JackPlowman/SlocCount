# Install python dependencies
install:
    uv sync --all-extras

# Validate the JSON schema
validate-schema:
    uv run check-jsonschema --schemafile schema_validation/output_schema.json schema_validation/output.json

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
