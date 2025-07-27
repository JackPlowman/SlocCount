from pydantic import BaseModel


class Commit(BaseModel):
    """Pydantic model for Commit."""

    id: str
    date: str
    total_files: int
    total_lines: int


class Summary(BaseModel):
    """Pydantic model for Summary."""

    total_line_count: int
    total_file_count: int


class AnalysedRepository(BaseModel):
    """Pydantic model for AnalysedRepository."""

    name: str
    summary: Summary
    commits: list[Commit]

    class Config:
        """Pydantic configuration for AnalysedRepository."""

        arbitrary_types_allowed = True


class Total(BaseModel):
    """Pydantic model for Total."""

    lines: int
    files: int


class Output(BaseModel):
    """Pydantic model for Output."""

    total: Total
    repositories: list[AnalysedRepository]
