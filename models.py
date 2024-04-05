from database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, text, Time


class Hours(Base):
    __tablename__ = "hours"

    id = Column(Integer,primary_key=True,nullable=False)
    day = Column(Integer,nullable=False)
    restaurant = Column(String,nullable=False)
    open_hour = Column(Time,nullable=False)
    close_hour = Column(Time, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))