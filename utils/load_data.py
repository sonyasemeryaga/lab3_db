import pandas as pd
from datetime import datetime
from database.connection import get_session
from models.weather import Weather, WindDirection
from models.air_quality import AirQuality 

CSV_PATH = "GlobalWeatherRepository.csv"


def parse_datetime(val):
    try:
        return datetime.strptime(str(val), "%Y-%m-%d %H:%M")
    except:
        return None


def parse_wind_direction(val):
    try:
        return WindDirection(str(val).strip())
    except:
        return None


def load_data():
    print("Читаємо CSV...")
    df = pd.read_csv(CSV_PATH)
    print(f"Знайдено рядків: {len(df)}")

    session = get_session()

    try:
        for i, row in df.iterrows():
            record = Weather(
                country        = str(row["country"]),
                location_name  = str(row["location_name"]),
                last_updated   = parse_datetime(row["last_updated"]),
                wind_kph       = float(row["wind_kph"]),
                wind_degree    = int(row["wind_degree"]),
                wind_direction = parse_wind_direction(row["wind_direction"]),
                sunrise        = str(row["sunrise"]),

                air_quality_Carbon_Monoxide  = float(row["air_quality_Carbon_Monoxide"]),
                air_quality_Ozone            = float(row["air_quality_Ozone"]),
                air_quality_Nitrogen_dioxide = float(row["air_quality_Nitrogen_dioxide"]),
                air_quality_Sulphur_dioxide  = float(row["air_quality_Sulphur_dioxide"]),
                air_quality_PM25             = float(row["air_quality_PM2.5"]),
                air_quality_PM10             = float(row["air_quality_PM10"]),
                air_quality_us_epa_index     = int(row["air_quality_us-epa-index"]),
                air_quality_gb_defra_index   = int(row["air_quality_gb-defra-index"]),
            )
            session.add(record)

        session.commit()
        print(f"Готово! Завантажено {len(df)} рядків.")

    except Exception as e:
        session.rollback()
        print(f"Помилка: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    load_data()