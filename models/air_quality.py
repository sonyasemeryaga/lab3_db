from sqlalchemy import Column, Integer, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from models.weather import Base

class AirQuality(Base):
    __tablename__ = "air_quality"

    id               = Column(Integer, primary_key=True, autoincrement=True)
    weather_id       = Column(Integer, ForeignKey("weather.id"), nullable=False)

    carbon_monoxide  = Column(Float)
    ozone            = Column(Float)
    nitrogen_dioxide = Column(Float)
    sulphur_dioxide  = Column(Float)
    pm25             = Column(Float)
    pm10             = Column(Float)
    us_epa_index     = Column(Integer)
    gb_defra_index   = Column(Integer)
    is_safe_to_go_outside = Column(Boolean, nullable=True)

    weather = relationship("Weather", back_populates="air_quality")

    def __repr__(self):
        return f"<AirQuality(weather_id={self.weather_id}, pm25={self.pm25})>"