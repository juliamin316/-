import requests
from bs4 import BeautifulSoup
import csv

url = "https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D0%B3%D0%BE%D1%81%D1%83%D0%B4%D0%B0%D1%80%D1%81%D1%82%D0%B2_%D0%B8_%D0%B7%D0%B0%D0%B2%D0%B8%D1%81%D0%B8%D0%BC%D1%8B%D1%85_%D1%82%D0%B5%D1%80%D1%80%D0%B8%D1%82%D0%BE%D1%80%D0%B8%D0%B9_%D0%BF%D0%BE_%D0%BD%D0%B0%D1%81%D0%B5%D0%BB%D0%B5%D0%BD%D0%B8%D1%8E"

response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

try:
    table = soup.find("table", class_="standard sortable jquery-tablesorter")

    if not table:
        tables = soup.find_all("table")
        for t in tables:
            caption = t.find("caption")
            if caption and "Страны и их население" in caption.text:
                table = t
                break

    if not table:
        raise ValueError("Таблица не найдена. Проверьте класс таблицы или текст подписи.")

    # Список для хранения данных
    countries_population = []

    # Парсим строки таблицы
    for row in table.find("tbody").find_all("tr"):
        cells = row.find_all("td")
        if len(cells) >= 3:
            country_span = cells[1].find("span", class_="nowrap")
            country_name = country_span["data-sort-value"].strip() if country_span and "data-sort-value" in country_span.attrs else cells[1].text.strip()
            population = cells[2].text.strip()
            countries_population.append((country_name, population))

    with open("население.csv", "w", newline="", encoding="utf-8") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["Страна", "Население"])
        csvwriter.writerows(countries_population)

    print("Данные успешно сохранены в файл 'население.csv'.")

except Exception as e:
    print(f"Ошибка: {e}")
