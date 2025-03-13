from structlog import get_logger, stdlib

from .configuration import Configuration
from .custom_logging import set_up_custom_logging
from .github_interactions import clone_repo, retrieve_repositories

logger: stdlib.BoundLogger = get_logger()


def main() -> None:  # noqa: D103
    set_up_custom_logging()
    logger.info("Starting scanner")

    configuration = Configuration()
    repositories = retrieve_repositories(configuration)
    for repository in repositories:
        owner_name, repository_name = repository.owner.login, repository.name
        clone_repo(owner_name, repository_name)


if __name__ == "__main__":
    main()
