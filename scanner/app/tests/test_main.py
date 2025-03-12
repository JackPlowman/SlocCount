from unittest.mock import MagicMock, patch

from app.main import main

FILE_PATH = "app.main"


@patch(f"{FILE_PATH}.set_up_custom_logging")
def test_main(mock_set_up_custom_logging: MagicMock) -> None:
    """Test the main function."""
    # Arrange
    # Act
    main()
    # Assert
    mock_set_up_custom_logging.assert_called_once_with()
