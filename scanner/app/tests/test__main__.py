from unittest.mock import MagicMock, patch

from scanner.app.__main__ import (
    AnalysedRepository,
    Configuration,
    analyse_repository_files,
    clean_up,
    generate_output,
    main,
    run_analyser,
    timeline_analysis,
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
@patch(f"{FILE_PATH}.timeline_analysis")
@patch(f"{FILE_PATH}.analyse_repository_files")
@patch(f"{FILE_PATH}.clone_repo")
@patch(f"{FILE_PATH}.retrieve_repositories")
@patch(f"{FILE_PATH}.ProjectSummary")
def test_run_analyser(
    mock_project_summary: MagicMock,
    mock_retrieve_repositories: MagicMock,
    mock_clone_repo: MagicMock,
    _mock_analyse_repository_files: MagicMock,
    mock_timeline_analysis: MagicMock,
    mock_generate_output: MagicMock,
) -> None:
    """Test the run_analyser function."""
    # Arrange
    mock_configuration = MagicMock(spec=Configuration)
    repository_mock = MagicMock(owner=MagicMock(login="owner"))
    mock_retrieve_repositories.return_value = [repository_mock]
    mock_clone_repo.return_value = "cloned_repositories/repo"
    mock_project_summary.return_value = MagicMock()

    # Act
    run_analyser(mock_configuration)

    # Assert
    mock_retrieve_repositories.assert_called_once_with(mock_configuration)
    mock_clone_repo.assert_called_once_with("owner", repository_mock.name)
    mock_generate_output.assert_called_once_with(
        [
            {
                "name": repository_mock.name,
                "summary": mock_project_summary.return_value,
                "commits": mock_timeline_analysis.return_value,
            }
        ]
    )


@patch(f"{FILE_PATH}.ProjectSummary")
@patch(f"{FILE_PATH}.SourceAnalysis")
@patch(f"{FILE_PATH}.Path")
def test_analyse_repository_files(
    mock_path: MagicMock,
    mock_source_analysis: MagicMock,
    mock_project_summary: MagicMock,
) -> None:
    """Test the analyse_repository_files function."""
    # Arrange
    folder_path = "test_folder"
    repository_name = "test_repo"
    mock_root = MagicMock()
    mock_root.parts = ("root",)
    mock_root.__str__.return_value = "root"
    mock_path.return_value.walk.return_value = [(mock_root, [], ["file.py"])]
    # Act
    analyse_repository_files(mock_project_summary, folder_path, repository_name)
    # Assert
    mock_path.assert_called_once_with(folder_path)
    mock_source_analysis.from_file.assert_called_once_with(
        str(mock_root.__truediv__("file.py")), repository_name
    )
    mock_project_summary.add.assert_called_once_with(
        mock_source_analysis.from_file.return_value
    )


@patch(f"{FILE_PATH}.ProjectSummary")
@patch(f"{FILE_PATH}.analyse_repository_files")
@patch(f"{FILE_PATH}.Repo")
def test_timeline_analysis(
    mock_repo: MagicMock,
    mock_analyse_repository_files: MagicMock,
    mock_project_summary: MagicMock,
) -> None:
    """Test the timeline_analysis function."""
    # Arrange
    commit = MagicMock()
    mock_repo.return_value.iter_commits.return_value = [commit]
    folder_path = "test_folder"
    repository_name = "test_repo"
    # Act
    timeline_analysis(folder_path, repository_name)
    # Assert
    mock_analyse_repository_files.assert_called_once_with(
        mock_project_summary.return_value, folder_path, repository_name
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
            "commits": [],
        },
        {
            "name": "repo2",
            "summary": MagicMock(total_line_count=200, total_file_count=20),
            "commits": [],
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
                {
                    "name": "repo1",
                    "summary": {"lines": 100, "files": 10},
                    "commits": [],
                },
                {
                    "name": "repo2",
                    "summary": {"lines": 200, "files": 20},
                    "commits": [],
                },
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
