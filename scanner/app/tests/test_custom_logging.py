from logging import DEBUG, INFO
from os import environ
from unittest.mock import patch

import pytest
from structlog import get_logger

from app.custom_logging import set_up_custom_logging


@pytest.mark.parametrize(
    ("debug_env", "expected_level"), [("false", INFO), ("true", DEBUG)]
)
@patch.dict(environ, {}, clear=True)
def test_set_up_custom_logging(debug_env: str, expected_level: int) -> None:
    """Test the set_up_custom_logging function."""
    # Arrange
    environ["INPUT_DEBUG"] = debug_env
    # Act
    set_up_custom_logging()
    logger = get_logger()
    # Assert
    assert logger._logger.level == expected_level
