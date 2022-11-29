from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class _Person(BaseModel):
    uid: int
    ldap: str
    email: str
    extra_attributes: Dict[str, Any]
    last_update: str
    error_msg: str
    sync: bool


class _Events(BaseModel):
    start_event: str
    end_event: str
    person_uid: int


class _Calendar(BaseModel):
    uid: str
    name: str
    description: str
    category: str
    order: int
    last_update: str
    error_msg: str
    sync: bool
    events: List[_Events]


class _Config(BaseModel):
    text_color: str
    background_color: str
    categories: List[str]
    timezone: str


class CurrentSchedule(BaseModel):
    config: _Config
    calendars: List[_Calendar]
    persons: Dict[int, _Person]


class _ExtraInfoOnPerson(BaseModel):
    information: str
    icon: str
    icon_color: str
    url: Optional[str]


class PersonResponse(BaseModel):
    uid: str
    ldap: str
    email: str
    extra_attributes: List[_ExtraInfoOnPerson]
    last_update: str
    error_msg: str
    sync: bool
