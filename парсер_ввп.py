import requests
from bs4 import BeautifulSoup
import csv
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

url = "https://gogov.ru/articles/gdp-by-country"

# Настройка сессии для повторных попыток
session = requests.Session()
retry = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
adapter = HTTPAdapter(max_retries=retry)
session.mount("http://", adapter)
session.mount("https://", adapter)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

try:
    response = session.get(url, headers=headers)
    response.raise_for_status()  # Проверка на успешность запроса
    soup = BeautifulSoup(response.content, "html.parser")

    table = soup.find("table", id="m-table")

    if not table:
        raise ValueError("Таблица не найдена. Проверьте id или класс таблицы.")

    gdp_data = []

    for row in table.find("tbody").find_all("tr"):
        cells = row.find_all("td")
        if len(cells) >= 2:
            country_name = cells[0].text.strip()
            gdp_2024 = cells[1]["data-text"] if "data-text" in cells[1].attrs else cells[1].text.strip()
            gdp_data.append((country_name, gdp_2024))

    with open("ВВП.csv", "w", newline="", encoding="utf-8") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["Страна", "ВВП (номинальный, 2024, млрд $)"])
        csvwriter.writerows(gdp_data)

    print("Данные успешно сохранены в файл 'gdp_by_country.csv'.")

except requests.exceptions.RequestException as e:
    print(f"Ошибка при выполнении запроса: {e}")
except Exception as e:
    print(f"Ошибка: {e}")
