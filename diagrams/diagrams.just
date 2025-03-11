# ------------------------------------------------------------------------------
# Common Commands
# ------------------------------------------------------------------------------

# Install python dependencies
install:
    uv sync --all-extras

# Create the C4 diagram
create-c4-diagram:
    uv run python c4.py
