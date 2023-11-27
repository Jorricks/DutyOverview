from pathlib import Path
from typing import ClassVar, List

from sqlalchemy.orm import Session as SASession

from duty_board.models.person import Person
from duty_board.plugin.abstract_plugin import AbstractPlugin
from duty_board.plugin.ical_plugin_mixin import ICalPluginMixin


class ExamplePlugin(ICalPluginMixin, AbstractPlugin):
    absolute_path_to_favicon_ico = Path(__file__).resolve().parent / "favicon.ico"
    absolute_path_to_company_logo_png = Path(__file__).resolve().parent / "example_logo.png"
    category_order: ClassVar[List[str]] = ["Big Data", "Infrastructure"]

    def sync_person(self, person: Person, session: SASession) -> Person:  # noqa: ARG002
        """This is to be implemented by our end user."""
        return person

    # sync_calendar is implemented by the ICalPluginMixin.

    async def admin_login_attempt(self, username: str, password: str) -> bool:
        return username == "admin" and password == "admin123"  # noqa: S105
