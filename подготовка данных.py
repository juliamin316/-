# Первая часть обработки 
import pandas as pd

file_paths = [
    '/content/перевод (1).csv',  
    '/content/население.csv', 
    '/content/Продолжительность жизни.csv',  
    '/content/Индекс человеческого развития.csv',  
    '/content/ВВП.csv'   
]


merged_df = pd.read_csv(file_paths[0])

for file in file_paths[1:]:

    df = pd.read_csv(file)
    
    merged_df = pd.merge(merged_df, df, on='Страна', how='outer')

merged_df.to_csv('data.csv', index=False, encoding='utf-8')

print("Общий файл успешно создан и сохранён как 'data.csv'")
# Вторая часть обработки
import pandas as pd

file_path = '/content/data.csv'
data = pd.read_csv(file_path)
data_cleaned = data.dropna()

data_cleaned.to_csv('очищенные_данные.csv', index=False, encoding='utf-8')

print("Данные сохранены в файл 'очищенные_данные.csv'")
