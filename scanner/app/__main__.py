from pathlib import Path
from shutil import rmtree

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
        clone_repo(owner_name, repository_name)


def clean_up() -> None:
    """Clean up the cloned repositories."""
    logger.debug("Cleaning up cloned repositories")
    cloned_repositories = Path("cloned_repositories")
    for repository in cloned_repositories.iterdir():
        if repository.is_dir():
            rmtree(repository)


if __name__ == "__main__":
    main()
