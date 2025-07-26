from json import dump
from pathlib import Path

from git import rmtree
from structlog import get_logger, stdlib

from .analysis import run_analyser
from .configuration import Configuration
from .custom_logging import set_up_custom_logging
from .custom_types import AnalysedRepository

logger: stdlib.BoundLogger = get_logger()


def main() -> None:  # noqa: D103
    set_up_custom_logging()

    logger.info("Starting scanner")
    configuration = Configuration()
    try:
        analysis = run_analyser(configuration)
        generate_output(analysis)
    except:
        logger.exception("An error occurred during analysis")
        raise
    finally:
        clean_up()
    logger.info("Finished scanner")


def generate_output(analysis: list[AnalysedRepository]) -> None:
    """Generate output from the analysis."""
    total_code_lines = sum(
        repository["summary"].total_line_count for repository in analysis
    )
    total_files = sum(repository["summary"].total_file_count for repository in analysis)
    dict_to_json = {
        "total": {
            "lines": total_code_lines,
            "files": total_files,
        },
        "repositories": [
            {
                "name": repository["name"],
                "summary": {
                    "lines": repository["summary"].total_line_count,
                    "files": repository["summary"].total_file_count,
                },
                "commits": repository["commits"],
            }
            for repository in analysis
        ],
    }
    with Path("output.json").open("w", encoding="utf-8") as file:
        dump(dict_to_json, file, indent=4, ensure_ascii=False)


def clean_up() -> None:
    """Clean up the cloned repositories."""
    logger.debug("Cleaning up cloned repositories")
    cloned_repositories = Path("cloned_repositories")
    for repository in cloned_repositories.iterdir():
        if repository.is_dir():
            rmtree(repository)


if __name__ == "__main__":
    main()
