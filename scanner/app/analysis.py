from pathlib import Path
from timeit import default_timer

from git import Repo
from pygount import ProjectSummary, SourceAnalysis
from structlog import get_logger, stdlib

from .configuration import Configuration
from .custom_types import AnalysedRepository
from .github_interactions import clone_repo, retrieve_repositories

logger: stdlib.BoundLogger = get_logger()
IGNORE_FOLDERS = [".git"]
IGNORE_FILES = [".gitignore", ".json", ".lock"]


def run_analyser(configuration: Configuration) -> list[AnalysedRepository]:
    """Run the analyser.

    This function is a placeholder for the actual analysis logic.
    """
    repositories = retrieve_repositories(configuration)
    analysis: list[AnalysedRepository] = []
    total_repositories = len(list(repositories))
    for index, repository in enumerate(repositories):
        start_time = default_timer()
        owner_name, repository_name = repository.owner.login, repository.name
        folder_path = clone_repo(owner_name, repository_name)
        project_summary = ProjectSummary()
        analyse_repository_files(project_summary, folder_path, repository_name)
        commits_analysis = timeline_analysis(folder_path, repository_name)
        analysis.append(
            {
                "name": repository_name,
                "summary": project_summary,
                "commits": commits_analysis,
            }
        )
        logger.info(
            "Project summary",
            repository=repository_name,
            project_summary=project_summary,
            progress=f"{index + 1}/{total_repositories}",
            progress_percentage=f"{(index + 1) / total_repositories * 100:.2f}%",
            analysis_elapsed_time=f"{default_timer() - start_time:.2f} seconds",
        )
    return analysis


def analyse_repository_files(
    project_summary: ProjectSummary, folder_path: str, repository_name: str
) -> None:
    """Analyse the files in the repository.

    This function iterates through the files in the repository and performs analysis
    on each file, adding the results to the project summary.

    Args:
        project_summary (ProjectSummary): The summary object to which file analyses
            are added.
        folder_path (str): The path to the cloned repository folder.
        repository_name (str): The name of the repository being analysed.
    """
    iterator = Path(folder_path).walk()
    for _root, _dirs, files in iterator:
        if any(folder in _root.parts for folder in IGNORE_FOLDERS):
            logger.debug("Skipping folder", folder=_root)
            continue
        files_minus_excluded = [
            file
            for file in files
            if not any(file.endswith(ignore) for ignore in IGNORE_FILES)
            or any(file == ignore for ignore in IGNORE_FILES)
        ]
        for file in files_minus_excluded:
            file_path = str(_root / file)
            logger.debug("Analysing file", file=file_path)
            file_analysis = SourceAnalysis.from_file(file_path, repository_name)
            logger.debug("File analysis", file_analysis=file_analysis)
            if file_analysis.language not in [
                "__unknown__",
                "__empty__",
                "__error__",
                "__binary__",
            ]:
                project_summary.add(file_analysis)


def timeline_analysis(file_path: str, repository_name: str) -> list[dict]:
    """Perform timeline analysis on the project summary.

    This function is a placeholder for the actual timeline analysis logic.
    Currently, it does not perform any operations.

    Args:
        file_path (str): The path to the cloned repository folder.
        repository_name (str): The name of the repository being analysed.

    Returns:
        list[dict]: A list of dictionaries containing commit details.
    """
    logger.debug("Performing timeline analysis")
    repository = Repo(file_path)
    timeline_data = []
    commits = list(repository.iter_commits())
    logger.debug("Total commits found", total_commits=len(commits))
    for index, commit in enumerate(commits):
        if index > 10:  # Limit to first 10 commits for performance
            break
        logger.debug(
            "Commit Analysis",
            commit=commit,
            commit_date=commit.committed_datetime.isoformat(),
            commit_percentage=index + 1 / len(commits),
        )
        repository.git.checkout(commit.hexsha)
        project_summary = ProjectSummary()
        analyse_repository_files(project_summary, file_path, repository_name)
        logger.debug("Project summary", project_summary=project_summary)
        timeline_data.append(
            {
                "commit": commit.hexsha,
                "commit_date": commit.committed_datetime.isoformat(),
                "message": commit.message,
                "total_files": project_summary.total_file_count,
                "total_lines": project_summary.total_line_count,
            }
        )

    return timeline_data
