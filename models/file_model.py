

from sqlalchemy.orm import mapped_column

from sqlalchemy import (
    ForeignKey, Integer, Text, DateTime, Boolean,
    LargeBinary
)

import sqlalchemy as sa

from helpers.db_helper import Base

#Base = declarative_base # deprecated

class FileTable(Base):
    __tablename__ = 'file_table'
    id =  mapped_column(Integer, sa.Identity(), primary_key = True, nullable = False)
    file_name = mapped_column(Text, nullable = False)
    file_type = mapped_column(Text, nullable = False)
    file_data = mapped_column(LargeBinary, nullable=False)
    project_id = mapped_column(Integer, nullable = True) #nullable for profile uploads
    is_profile = mapped_column(Boolean, nullable = False)
    user_id = mapped_column(
            Integer,
            ForeignKey('user_table.id', ondelete = 'CASCADE'),
            nullable = False
        )
    date_time = mapped_column(DateTime(timezone=True), nullable = False)


    def __repr__(self):
        return f'<file id {self.id}>'