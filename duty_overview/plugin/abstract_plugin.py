from __future__ import annotations

import datetime
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Optional

from duty_overview.alchemy.session import create_session
from duty_overview.models.on_call_event import OnCallEvent
from sqlalchemy.orm import Session as SASession

from duty_overview.models.calendar import Calendar
from duty_overview.models.person import Person
from duty_overview.plugin.helpers.duty_calendar_config import DutyCalendarConfig


class AbstractPlugin(ABC):
    admin_session_length: datetime.timedelta = datetime.timedelta(days=7)
    person_update_frequency: datetime.timedelta = datetime.timedelta(hours=1)
    calendar_update_frequency: datetime.timedelta = datetime.timedelta(days=1)
    background_color_hex: str = "#3C9C2D"
    text_color_hex: str = "white"
    absolute_path_to_company_logo_png: Path | None = None
    absolute_path_to_user_images_folder: Path | None = None
    category_order: List[str] = []
    duty_calendar_configurations: List[DutyCalendarConfig] = []
    enable_admin_button: bool = True
    git_repository_url: Optional[str] = "https://github.com/Jorricks/DutyOverview"

    @abstractmethod
    def sync_person(self, person: Person, session: SASession) -> Person:
        pass

    @abstractmethod
    def sync_calendar(self, calendar: Calendar, event_prefix: str | None, session: SASession) -> Calendar:
        pass

    @abstractmethod
    async def admin_login_attempt(self, username: str, password: str) -> bool:
        pass
