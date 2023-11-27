from typing import Optional

from pendulum.datetime import DateTime
from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from duty_board.alchemy.settings import Base
from duty_board.alchemy.sqlalchemy_types import UtcDateTime
from duty_board.models.person_image import PersonImage


class Person(Base):
    __table_args__ = (UniqueConstraint("image_uid", name="unique_image_uid"),)  # To make sure it remains a one-to-one.
    __tablename__ = "person"
    uid: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)
    username: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, unique=True)
    email: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, unique=True)

    image_uid: Mapped[Optional[int]] = mapped_column(ForeignKey("person_image.uid"), nullable=True)
    image: Mapped[Optional[PersonImage]] = relationship(
        back_populates="person",
        cascade="all, delete-orphan",
        single_parent=True,  # delete orphans :)
    )

    img_width: Mapped[Optional[int]]
    img_height: Mapped[Optional[int]]
    extra_attributes_json: Mapped[Optional[str]] = mapped_column(
        String(100000),
        nullable=True,
        comment="Extra attributes represented as a json.",
    )
    error_msg: Mapped[Optional[str]] = mapped_column(
        String(9999),
        nullable=True,
        comment="If any, the error of the latest sync attempt.",
    )
    last_update_utc: Mapped[DateTime] = mapped_column(UtcDateTime(), nullable=False)
    sync: Mapped[bool] = mapped_column(default=True)

    def __repr__(self) -> str:
        return f"Person(username='{self.username}', email='{self.email}')"
