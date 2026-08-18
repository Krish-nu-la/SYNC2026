from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean

from app.database.database import Base


class Report(Base):

    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)

    zone = Column(String, index=True)

    description = Column(String, nullable=True)

    severity = Column(String, nullable=False)

    latitude = Column(Float, nullable=False)

    longitude = Column(Float, nullable=False)

    depth_cm = Column(Float, nullable=True)

    road_blocked = Column(Boolean, default=False)

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        index=True
    )