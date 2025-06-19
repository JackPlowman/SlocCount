# Install python dependencies
install:
    uv sync --all-extras

# Validate the JSON schema
validate-schema:
    uv run check-jsonschema --schemafile schema_validation/output_schema.json schema_validation/output.json

# ------------------------------------------------------------------------------
# Ruff - Python Linting and Formatting
# ------------------------------------------------------------------------------

# Fix all Ruff issues
ruff-fix:
    just tests::ruff-format-fix
    just tests::ruff-lint-fix

# Check for all Ruff issues
ruff-checks:
    just tests::ruff-format-check
    just tests::ruff-lint-check

# Check for Ruff issues
ruff-lint-check:
    uv run ruff check .

# Fix Ruff lint issues
ruff-lint-fix:
    uv run ruff check . --fix --unsafe-fixes

# Check for Ruff format issues
ruff-format-check:
    uv run ruff format --check .

# Fix Ruff format issues
ruff-format-fix:
    uv run ruff format .

# ------------------------------------------------------------------------------
# Ty - Python Type Checking
# ------------------------------------------------------------------------------

# Check for type issues with Ty
ty-check:
    uv run ty check .

# ------------------------------------------------------------------------------
# Other Python Tools
# ------------------------------------------------------------------------------

# Check uv lockfile
uv-lock-check:
    uv lock --check
