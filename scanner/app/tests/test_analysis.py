from unittest.mock import MagicMock, patch

from scanner.app.analysis import (
    Configuration,
    analyse_repository_files,
    run_analyser,
    timeline_analysis,
)
from scanner.app.custom_types import AnalysedRepository, Summary

FILE_PATH = "scanner.app.analysis"


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
    _mock_timeline_analysis: MagicMock,
) -> None:
    """Test the run_analyser function."""
    # Arrange
    mock_configuration = MagicMock(spec=Configuration)
    repository_mock = MagicMock(owner=MagicMock(login="owner"))
    repository_mock.name = "repo"
    mock_retrieve_repositories.return_value = [repository_mock]
    mock_clone_repo.return_value = "cloned_repositories/repo"
    mock_project_summary.return_value = MagicMock(
        total_line_count=100, total_file_count=10
    )
    # Act
    analysis = run_analyser(mock_configuration)

    # Assert
    mock_retrieve_repositories.assert_called_once_with(mock_configuration)
    mock_clone_repo.assert_called_once_with("owner", repository_mock.name)
    assert [
        AnalysedRepository(
            name="repo",
            summary=Summary(total_line_count=100, total_file_count=10),
            commits=[],
        )
    ] == analysis


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
    commit.hexsha = "1234567890abcdef"
    commit.message = "Initial commit"
    commit.committed_datetime.isoformat.return_value = "2023-10-01T12:00:00Z"
    mock_repo.return_value.iter_commits.return_value = [commit]
    folder_path = "test_folder"
    repository_name = "test_repo"
    # Act
    timeline_analysis(folder_path, repository_name)
    # Assert
    mock_analyse_repository_files.assert_called_once_with(
        mock_project_summary.return_value, folder_path, repository_name
    )
