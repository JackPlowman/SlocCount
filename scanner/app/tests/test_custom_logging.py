from os import environ
from unittest.mock import patch

import pytest

from app.custom_logging import set_up_custom_logging


@pytest.mark.parametrize(("debug_env"), [("false"), ("true")])
@patch.dict(environ, {}, clear=True)
def test_set_up_custom_logging(debug_env: str) -> None:
    """Test the set_up_custom_logging function."""
    # Arrange
    environ["INPUT_DEBUG"] = debug_env
    # Act
    set_up_custom_logging()
