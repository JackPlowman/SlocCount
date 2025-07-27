from unittest.mock import MagicMock, patch

from scanner.app.__main__ import (
    AnalysedRepository,
    clean_up,
    generate_output,
    main,
)
from scanner.app.custom_types import Summary

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


@patch(f"{FILE_PATH}.Path")
@patch(f"{FILE_PATH}.dump")
def test_generate_output(mock_dump: MagicMock, mock_path: MagicMock) -> None:
    """Test the generate_output function."""
    # Arrange
    analysis = [
        AnalysedRepository(
            name="repo1",
            summary=Summary(total_line_count=100, total_file_count=10),
            commits=[],
        ),
        AnalysedRepository(
            name="repo2",
            summary=Summary(total_line_count=200, total_file_count=20),
            commits=[],
        ),
    ]
    mock_file = MagicMock()
    mock_path.return_value.open.return_value.__enter__.return_value = mock_file
    # Act
    generate_output(analysis)
    # Assert
    mock_path.return_value.open.assert_called_once_with("w", encoding="utf-8")
    mock_dump.assert_called_once_with(
        {
            "total": {"lines": 300, "files": 30},
            "repositories": [
                {
                    "name": "repo1",
                    "summary": {"total_line_count": 100, "total_file_count": 10},
                    "commits": [],
                },
                {
                    "name": "repo2",
                    "summary": {"total_line_count": 200, "total_file_count": 20},
                    "commits": [],
                },
            ],
        },
        mock_file,
        indent=4,
        ensure_ascii=False,
    )


@patch(f"{FILE_PATH}.rmtree")
@patch(f"{FILE_PATH}.Path")
def test_clean_up(mock_path: MagicMock, mock_rmtree: MagicMock) -> None:
    """Test the clean_up function."""
    # Arrange
    mock_repository = MagicMock(is_dir=MagicMock(return_value=True))
    mock_path.return_value.iterdir.return_value = [mock_repository]
    # Act
    clean_up()
    # Assert
    mock_rmtree.assert_called_once_with(mock_repository)
    mock_path.return_value.iterdir.assert_called_once_with()
