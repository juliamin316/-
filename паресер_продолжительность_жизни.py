import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://gtmarket.ru/ratings/life-expectancy-index'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

table = soup.find('table', {'id': 'study-dataset-life-expectancy-index'})

countries = []
overall_life_expectancy = []
men_life_expectancy = []
women_life_expectancy = []

rows = table.find_all('tr')[2:]

for row in rows:
    columns = row.find_all('td')
    if len(columns) > 0:
        country = columns[1].get_text(strip=True)
        overall = columns[2].get_text(strip=True)
        men = columns[3].get_text(strip=True)
        women = columns[4].get_text(strip=True)

        countries.append(country)
        overall_life_expectancy.append(overall)
        men_life_expectancy.append(men)
        women_life_expectancy.append(women)

# Создаем DataFrame
data = {
    'Country': countries,
    'Life Expectancy (All)': overall_life_expectancy,
    'Life Expectancy (Men)': men_life_expectancy,
    'Life Expectancy (Women)': women_life_expectancy
}

df = pd.DataFrame(data)

df.to_csv('Продолжительность жизни.csv', index=False, encoding='utf-8')

print("Данные сохранены в файл 'продолжительность жизни.csv'")
