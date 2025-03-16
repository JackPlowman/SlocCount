from unittest.mock import MagicMock, patch

from scanner.app.__main__ import Configuration, main, run_analyser

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


@patch(f"{FILE_PATH}.SourceAnalysis")
@patch(f"{FILE_PATH}.clone_repo")
@patch(f"{FILE_PATH}.retrieve_repositories")
@patch(f"{FILE_PATH}.ProjectSummary")
@patch(f"{FILE_PATH}.Path")
def test_run_analyser(
    mock_path: MagicMock,
    mock_project_summary: MagicMock,
    mock_retrieve_repositories: MagicMock,
    mock_clone_repo: MagicMock,
    mock_source_analysis: MagicMock,
) -> None:
    """Test the run_analyser function."""
    # Arrange
    mock_configuration = MagicMock(spec=Configuration)
    repository_mock = MagicMock(owner=MagicMock(login="owner"))
    mock_retrieve_repositories.return_value = [repository_mock]
    mock_clone_repo.return_value = "cloned_repositories/repo"
    mock_path.return_value.walk.return_value = [("root", [], ["file.py"])]
    mock_project_summary.return_value = MagicMock()

    # Act
    run_analyser(mock_configuration)

    # Assert
    mock_retrieve_repositories.assert_called_once_with(mock_configuration)
    mock_clone_repo.assert_called_once_with("owner", repository_mock.name)
    mock_path.assert_called_once_with("cloned_repositories/repo")
    mock_project_summary.return_value.add.assert_called()
    mock_source_analysis.from_file.assert_called_once_with(
        "root/file.py", repository_mock.name
    )
