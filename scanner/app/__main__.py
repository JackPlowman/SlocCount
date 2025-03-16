from pathlib import Path

from git import rmtree
from pygount import ProjectSummary, SourceAnalysis
from structlog import get_logger, stdlib

from .configuration import Configuration
from .custom_logging import set_up_custom_logging
from .github_interactions import clone_repo, retrieve_repositories

logger: stdlib.BoundLogger = get_logger()


def main() -> None:  # noqa: D103
    set_up_custom_logging()
    logger.info("Starting scanner")
    configuration = Configuration()
    try:
        run_analyser(configuration)
    except:
        logger.exception("An error occurred during analysis")
        raise
    finally:
        clean_up()
    logger.info("Finished scanner")


def run_analyser(configuration: Configuration) -> None:
    """Run the analyser.

    This function is a placeholder for the actual analysis logic.
    """
    repositories = retrieve_repositories(configuration)
    for repository in repositories:
        owner_name, repository_name = repository.owner.login, repository.name
        folder_path = clone_repo(owner_name, repository_name)
        project_summary = ProjectSummary()
        iterator = Path(folder_path).walk()
        for _root, _dirs, files in iterator:
            for file in files:
                file_path = f"{_root.__str__()}/{file}"
                logger.debug("Analysing file", file=file_path)
                file_analysis = SourceAnalysis.from_file(file_path, repository_name)
                logger.debug("File analysis", file_analysis=file_analysis)
                if file_analysis.language not in [
                    "__unknown__",
                    "__empty__",
                    "__error__",
                ]:
                    project_summary.add(file_analysis)
        logger.info("Project summary", project_summary=project_summary)


def clean_up() -> None:
    """Clean up the cloned repositories."""
    logger.debug("Cleaning up cloned repositories")
    cloned_repositories = Path("cloned_repositories")
    for repository in cloned_repositories.iterdir():
        if repository.is_dir():
            rmtree(repository)


if __name__ == "__main__":
    main()
