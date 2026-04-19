from sqlalchemy.orm import joinedload
from models.weather import Weather
from models.air_quality import AirQuality

def get_weather_by_country_and_date(session, country, date):
    return (
        session.query(Weather)
        .options(joinedload(Weather.air_quality))
        .filter(
            Weather.country.ilike(f"%{country}%"),
            Weather.last_updated >= date,
            Weather.last_updated < date.replace(day=date.day + 1)
        )
        .all()
    )

def country_exists(session, country):
    return (
        session.query(Weather)
        .filter(Weather.country.ilike(f"%{country}%"))
        .first()
    )