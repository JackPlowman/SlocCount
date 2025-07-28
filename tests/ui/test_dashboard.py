
from playwright.sync_api import Page, expect

from .utils.environment_variables import PROJECT_URL


def test_title(page: Page) -> None:
    """Test that the title of the dashboard is correct."""
    # Act
    page.goto(PROJECT_URL)
    # Assert
    expect(page).to_have_title("SlocCount")
