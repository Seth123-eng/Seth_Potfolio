
from sqlalchemy.orm import mapped_column

from sqlalchemy import (
    Integer, Text, DateTime, ForeignKey,
    Boolean
)

import sqlalchemy as sa

from helpers.db_helper import Base


class MessageTable(Base):
    __tablename__ = 'message_table'
    id = mapped_column(Integer, sa.Identity(), primary_key = True, autoincrement = True)
    date_time = mapped_column(DateTime(timezone=True), nullable = False)
    message_description = mapped_column(Text, nullable = False)
    is_read=mapped_column(Boolean, nullable=False, default=False)
    email = mapped_column(Text, nullable = False)
    message_replied=mapped_column(Boolean, nullable=False, default=False)
    user_id = mapped_column( #0 for anonymous users
        Integer,
        ForeignKey('user_table.id', ondelete = 'CASCADE'),
        nullable = False
    )

    def __repr__(self) -> str:
        return f"<support center id = {self.id}>"