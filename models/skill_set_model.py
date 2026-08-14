

from sqlalchemy.orm import mapped_column

from sqlalchemy import (
    ForeignKey, Integer, Text, DateTime
)

import sqlalchemy as sa

from helpers.db_helper import Base

#Base = declarative_base # deprecated

class SkillSetTable(Base):
    __tablename__ = 'skill_set_table'
    id =  mapped_column(Integer, sa.Identity(), primary_key = True, nullable = False)
    skill_set_title = mapped_column(Text, nullable = True)
    skill_set_description = mapped_column(Text, nullable = True)
    user_id = mapped_column(
            Integer,
            ForeignKey('user_table.id', ondelete = 'CASCADE'),
            nullable = False
        )
    date_time = mapped_column(DateTime(timezone=True), nullable = False)


    def __repr__(self):
        return f'<file id {self.id}>'