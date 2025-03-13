from os import environ

from scanner.app.configuration import Configuration


def test_configuration() -> None:
    # Arrange
    environ["REPOSITORY_OWNER"] = repo_owner = "test2"
    environ["GITHUB_TOKEN"] = fake_token = "TestToken"  # noqa: S105
    configuration = Configuration()
    # Assert
    assert configuration.repository_owner == repo_owner
    assert configuration.github_token == fake_token
    # Clean Up
    del environ["REPOSITORY_OWNER"]
    del environ["GITHUB_TOKEN"]
