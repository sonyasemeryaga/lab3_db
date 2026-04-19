from datetime import datetime, timedelta
from database.connection import get_session
from repository.weather_repository import get_weather_by_country_and_date

def print_weather(record):
    print(f"\nПогода для {record.location_name}, {record.country} станом на {record.last_updated.strftime('%Y-%m-%d %H:%M')}")
    print(f"Країна: {record.country}")
    print(f"Місто: {record.location_name}")
    print(f"Дата: {record.last_updated}")
    print(f"Вітер: {record.wind_kph} км/г, {record.wind_degree}°, {record.wind_direction.value if record.wind_direction else 'N/A'}")
    print(f"Схід сонця: {record.sunrise}")

    if record.air_quality:
        aq = record.air_quality
        print(f"\nСтан повітря")
        print(f"PM2.5: {aq.pm25} мкг/м³")
        print(f"PM10: {aq.pm10} мкг/м³")
        print(f"Озон:{aq.ozone} мкг/м³")
        print(f"CO: {aq.carbon_monoxide} мкг/м³")
        print(f"NO2: {aq.nitrogen_dioxide} мкг/м³")
        print(f"SO2: {aq.sulphur_dioxide} мкг/м³")
        print(f"EPA індекс: {aq.us_epa_index}")
        print(f"DEFRA індекс: {aq.gb_defra_index}")
        safe = "Так" if aq.is_safe_to_go_outside else "Ні"
        print(f"Чи безпечно виходити на вулицю? {safe}")

def main():
    print("Пошук погодних даних по БД")
    country = input("Введіть країну (англійською мовою): ").strip()
    date_str = input("Введіть дату (у форматі YYYY-MM-DD): ").strip()

    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        print("Невірний формат дати! Будь ласка, використовуйте YYYY-MM-DD")
        return

    session = get_session()

    try:
        from repository.weather_repository import country_exists
        if not country_exists(session, country):
            print(f"\nКраїна '{country}' не знайдена в базі даних.")
            print("Перевірте правильність введення країни, назви країн вводяться англійською мовою.")
            return
        results = get_weather_by_country_and_date(session, country, date)
        if not results:
            print(f"\nКраїна '{country}' є в базі даних, але даних за {date_str} немає.")
            print("Спробуйте ввести іншу дату для отримання інформації.")
        else:
            print(f"\nЗнайдено {len(results)} записів:")
            for record in results:
                print_weather(record)
    finally:
        session.close()

if __name__ == "__main__":
    main()