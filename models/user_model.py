

from sqlalchemy.orm import Mapped, mapped_column, relationship

from sqlalchemy import (
    Integer, Text, DateTime
)

import sqlalchemy as sa

from datetime import datetime

from helpers.db_helper import Base

#Base = declarative_base # deprecated


from models.file_model import FileTable
from models.my_projects_model import MyProjectsTable
from models.personal_description_model import AboutMeTable
from models.message_model import MessageTable
from models.skill_set_model import SkillSetTable

class UserTable(Base):
    __tablename__ = 'user_table'
    id:Mapped[int] =  mapped_column(Integer, sa.Identity(), primary_key = True, nullable = False)
    account_type:Mapped[str] = mapped_column(Text, nullable = False) #admin, client
    user_name:Mapped[str] = mapped_column(Text, nullable = True)
    email:Mapped[str] = mapped_column(Text, nullable = False, unique = True)
    password_hash:Mapped[str] = mapped_column(Text, nullable = False)
    #time_zone:Mapped[str] = mapped_column(Text, nullable = True)
    date_time:Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable = False)


    #relationships
    files:Mapped[list[FileTable]] = relationship(
        backref="user_table",
        cascade="all, delete-orphan",
        passive_deletes=True,
        foreign_keys="FileTable.user_id"
    )

    my_projects:Mapped[list[MyProjectsTable]] = relationship(
        backref="user_table",
        cascade="all, delete-orphan",
        passive_deletes=True,
        foreign_keys="MyProjectsTable.user_id"
    )

    about_me:Mapped[AboutMeTable] = relationship(
        backref="user_table",
        cascade="all, delete-orphan",
        passive_deletes=True,
        foreign_keys="AboutMeTable.user_id"
    )

    messages:Mapped[list[MessageTable]] = relationship(
        backref="user_table",
        cascade="all, delete-orphan",
        passive_deletes=True,
        foreign_keys="MessageTable.user_id"
    )

    skill_sets:Mapped[list[SkillSetTable]] = relationship(
        backref="user_table",
        cascade="all, delete-orphan",
        passive_deletes=True,
        foreign_keys="SkillSetTable.user_id"
    )

    
    def __repr__(self):
        return f'<User id {self.id}>'