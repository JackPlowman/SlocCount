from unittest.mock import MagicMock, patch

from scanner.app.__main__ import (
    AnalysedRepository,
    Configuration,
    clean_up,
    generate_output,
    main,
    run_analyser,
)

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


@patch(f"{FILE_PATH}.generate_output")
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
    mock_generate_output: MagicMock,
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
    mock_generate_output.assert_called_once_with(
        [{"name": repository_mock.name, "summary": mock_project_summary.return_value}]
    )


@patch(f"{FILE_PATH}.Path")
@patch(f"{FILE_PATH}.dump")
def test_generate_output(mock_dump: MagicMock, mock_path: MagicMock) -> None:
    """Test the generate_output function."""
    # Arrange
    analysis: list[AnalysedRepository] = [
        {
            "name": "repo1",
            "summary": MagicMock(total_line_count=100, total_file_count=10),
        },
        {
            "name": "repo2",
            "summary": MagicMock(total_line_count=200, total_file_count=20),
        },
    ]
    mock_file = MagicMock()
    mock_path.return_value.open.return_value.__enter__.return_value = mock_file
    # Act
    generate_output(analysis)
    # Assert
    mock_dump.assert_called_once_with(
        {
            "total": {"lines": 300, "files": 30},
            "repositories": [
                {"name": "repo1", "summary": {"lines": 100, "files": 10}},
                {"name": "repo2", "summary": {"lines": 200, "files": 20}},
            ],
        },
        mock_file,
        indent=4,
        ensure_ascii=False,
    )
    mock_path.return_value.open.assert_called_once_with("w", encoding="utf-8")


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
