from unittest.mock import MagicMock, patch

from scanner.app.__main__ import main

FILE_PATH = "scanner.app.__main__"


@patch(f"{FILE_PATH}.run_analyser")
@patch(f"{FILE_PATH}.Configuration")
@patch(f"{FILE_PATH}.set_up_custom_logging")
def test_main(
    mock_set_up_custom_logging: MagicMock,
    mock_configuration: MagicMock,
    mock_run_analyser: MagicMock,
) -> None:
    """Test the main function."""
    # Arrange
    # Act
    main()
    # Assert
    mock_set_up_custom_logging.assert_called_once_with()
    mock_configuration.assert_called_once_with()
    mock_run_analyser.assert_called_once_with(mock_configuration.return_value)
