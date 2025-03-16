from typing import TypedDict

from pygount import ProjectSummary


class AnalysedRepository(TypedDict):
    """Repository information."""

    name: str
    summary: ProjectSummary
