import enum
from sqlalchemy import (
    Column, Integer, String, Float, DateTime,
    Enum as SAEnum
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class WindDirection(enum.Enum):
    N   = "N"
    NNE = "NNE"
    NE  = "NE"
    ENE = "ENE"
    E   = "E"
    ESE = "ESE"
    SE  = "SE"
    SSE = "SSE"
    S   = "S"
    SSW = "SSW"
    SW  = "SW"
    WSW = "WSW"
    W   = "W"
    WNW = "WNW"
    NW  = "NW"
    NNW = "NNW"


class Weather(Base):
    __tablename__ = "weather"

    id             = Column(Integer, primary_key=True, autoincrement=True)
    country        = Column(String(100), nullable=False)
    location_name  = Column(String(100))
    last_updated   = Column(DateTime)
    wind_kph       = Column(Float)
    wind_degree    = Column(Integer)
    wind_direction = Column(
        SAEnum(WindDirection, name="wind_direction_enum")
    )
    sunrise        = Column(String(20))

    air_quality_carbon_monoxide  = Column(Float)
    air_quality_ozone            = Column(Float)
    air_quality_nitrogen_dioxide = Column(Float)
    air_quality_sulphur_dioxide  = Column(Float)
    air_quality_pm25             = Column(Float)
    air_quality_pm10             = Column(Float)
    air_quality_us_epa_index     = Column(Integer)
    air_quality_gb_defra_index   = Column(Integer)

    air_quality = relationship("AirQuality", back_populates="weather", uselist=False)

    def __repr__(self):
        return f"<Weather(country={self.country}, date={self.last_updated})>"