from database.connection import get_session
from models.air_quality import AirQuality

def is_safe(pm25, ozone, us_epa_index,
            carbon_monoxide, nitrogen_dioxide,
            sulphur_dioxide, pm10):
    return (
        pm25 < 35 and
        ozone < 180 and
        us_epa_index <= 2 and
        carbon_monoxide < 10000 and
        nitrogen_dioxide < 200 and
        sulphur_dioxide < 500 and
        pm10 < 50
    )

def fill_safety_column():
    session = get_session()

    try:
        records = session.query(AirQuality).all()
        print(f"Обробляємо {len(records)} записів...")

        for record in records:
            record.is_safe_to_go_outside = is_safe(
                record.pm25,
                record.ozone,
                record.us_epa_index,
                record.carbon_monoxide,
                record.nitrogen_dioxide,
                record.sulphur_dioxide,
                record.pm10
            )

        session.commit()
        print("Готово! Колонка is_safe_to_go_outside заповнена.")

    except Exception as e:
        session.rollback()
        print(f"Помилка: {e}")
        raise
    finally:
        session.close()

if __name__ == "__main__":
    fill_safety_column()