from pathlib import Path
from timeit import default_timer

from date import today
from dateutil.relativedelta import relativedelta
from git import Repo
from pygount import ProjectSummary, SourceAnalysis
from structlog import get_logger, stdlib

from .configuration import Configuration
from .custom_types import AnalysedRepository, Commit, Summary
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
            AnalysedRepository(
                name=repository_name,
                summary=Summary(
                    total_line_count=project_summary.total_line_count,
                    total_file_count=project_summary.total_file_count,
                ),
                commits=commits_analysis,
            )
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


def timeline_analysis(file_path: str, repository_name: str) -> list[Commit]:
    """Perform timeline analysis on the project summary.

    This function analyses the first commit of each month from the repository's
    first commit to the current date. If no commit exists in a month, it uses
    the stats from the previous month.

    Args:
        file_path (str): The path to the cloned repository folder.
        repository_name (str): The name of the repository being analysed.

    Returns:
        list[Commit]: A list of Commit objects representing the timeline analysis.
    """
    logger.debug("Performing timeline analysis")
    repository = Repo(file_path)
    commits = list(repository.iter_commits())

    if not commits:
        logger.warning("No commits found in repository")
        return []

    first_commit = commits[0]
    first_commit_date = first_commit.committed_datetime.date()
    logger.warning(
        "First commit found",
        first_commit=first_commit.hexsha,
        first_commit_date=first_commit_date.isoformat(),
    )
    current_date = today()

    logger.debug(
        "Timeline analysis range",
        first_commit=first_commit.hexsha,
        first_commit_date=first_commit_date.strftime("%m/%Y"),
        current_date=current_date.strftime("%m/%Y"),
    )

    # Build monthly timeline
    timeline_data = []
    current_month = first_commit_date.replace(day=1)
    end_month = current_date.replace(day=1)
    logger.debug(
        "Timeline analysis months",
        start_month=current_month.strftime("%m/%Y"),
        end_month=end_month.strftime("%m/%Y"),
    )

    previous_month_data = None

    while current_month <= end_month:
        next_month = current_month + relativedelta(months=1)

        # Find first commit in this month
        month_commit = None
        for commit in commits:
            commit_date = commit.committed_datetime.date()
            if current_month <= commit_date < next_month:
                month_commit = commit
                break

        if month_commit:
            logger.debug(
                "Analysing commit for month",
                month=current_month.strftime("%m/%Y"),
                commit=month_commit.hexsha,
            )

            # Checkout and analyse this commit
            repository.git.checkout(month_commit.hexsha)
            project_summary = ProjectSummary()
            analyse_repository_files(project_summary, file_path, repository_name)

            commit_data = Commit(
                id=month_commit.hexsha,
                date=current_month.replace(day=1).isoformat(),
                total_files=project_summary.total_file_count,
                total_lines=project_summary.total_line_count,
            )
            timeline_data.append(commit_data)
            previous_month_data = commit_data

        elif previous_month_data:
            logger.debug(
                "No commit found for month, using previous month's data",
                month=current_month.strftime("%m/%Y"),
            )

            # Use previous month's data but update the date
            timeline_data.append(
                Commit(
                    id=previous_month_data.id,
                    date=current_month.replace(day=1).isoformat(),
                    total_files=previous_month_data.total_files,
                    total_lines=previous_month_data.total_lines,
                )
            )

        current_month = next_month

    logger.debug("Timeline analysis complete", total_months=len(timeline_data))
    return timeline_data
