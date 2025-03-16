# Install python dependencies
install:
    uv sync --all-extras

# Validate the JSON schema
validate-schema:
    uv run check-jsonschema --schemafile schema_validation/output_schema.json schema_validation/output.json
