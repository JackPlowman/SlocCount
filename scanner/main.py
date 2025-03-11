from .configuration import Configuration
from .github_interactions import clone_repo, retrieve_repositories


def main() -> None:  # noqa: D103
    configuration = Configuration()
    # Retrieve the list of repositories to analyse
    repositories = retrieve_repositories(configuration)
    # Set up data frame
    list_of_repositories = []  # noqa: F841
    # Create statistics for each repository
    for repository in repositories:
        owner_name, repository_name = repository.owner.login, repository.name
        # Clone the repository to cloned_repositories
        path = clone_repo(owner_name, repository_name)  # noqa: F841


if __name__ == "__main__":
    main()
