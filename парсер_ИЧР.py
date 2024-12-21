import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://gtmarket.ru/ratings/human-development-index'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

table = soup.find('table', {'id': 'study-dataset-human-development-index'})

countries = []
hd_indexes = []

rows = table.find_all('tr')[1:]

for row in rows:
    columns = row.find_all('td')
    if len(columns) > 0:
        country = columns[1].get_text(strip=True)
        hd_index = columns[2].get_text(strip=True)

        countries.append(country)
        hd_indexes.append(hd_index)

data = {
    'Страна': countries,
    'ИЧР': hd_indexes
}

df = pd.DataFrame(data)

df.to_csv('Индекс человеческого развития.csv', index=False, encoding='utf-8')

print("Данные сохранены в файл 'Индекс человеческого развития.csv'")
