pip install pandas dash plotly 

import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px
from dash.dependencies import Input, Output

df = pd.read_csv("очищенные_данные.csv")

# Преобразование данных
df['Население'] = df['Население'].str.replace(',', '').str.replace('\xa0', '').str.replace(' ', '').astype(float)
df['Площадь'] = df['Площадь'].astype(float)
df['Процент воды в территории'] = df['Процент воды в территории'].astype(float)
df['Продолжительность жизни (все)'] = df['Продолжительность жизни (все)'].astype(float)
df['ИЧР'] = df['ИЧР'].astype(float)
df['ВВП (номинальный, 2024, млрд $)'] = df['ВВП (номинальный, 2024, млрд $)'].astype(float)

# Создание приложения Dash
app = dash.Dash(__name__)

# Макет дашборда
app.layout = html.Div(style={'backgroundColor': '#111111'}, children=[  # Черный фон для всего приложения
    html.H1("Дашборд статистика по странам", 
            style={'text-align': 'center', 'color': 'white', 'font-family': 'Arial'}),  # Белый заголовок

    # Фильтр (Dropdown) для выбора стран
    html.Div([
        html.Label('Выберите страну:', style={'color': 'white'}),
        dcc.Dropdown(
            id='country_filter',
            options=[{'label': country, 'value': country} for country in df['Страна'].unique()],
            multi=True,  # Возможность выбирать несколько стран
            value=['Россия', 'Канада','Индия'],  # По умолчанию выбранные страны
            style={'width': '50%', 'color': 'black'}
        ),
    ], style={'margin': '20px', 'color': 'white'}),

    # График 1: Страна vs. Площадь (с фильтром)
    dcc.Graph(
        id='area_graph',
        figure=px.bar(df, x='Страна', y='Площадь', title='Площадь стран', color='Площадь', 
                      color_continuous_scale='Viridis', template='plotly_dark')
    ),

    # График 2: Продолжительность жизни по странам (с фильтром)
    dcc.Graph(
        id='life_expectancy_graph',
        figure=px.line(df, x='Страна', y='Продолжительность жизни (все)', title='Продолжительность жизни в разных странах', 
                       template='plotly_dark')
    ),

    # График 3: Индекс человеческого развития
    dcc.Graph(
        id='hdr_graph',
        figure=px.scatter(df, x='Страна', y='ИЧР', size='ИЧР', color='ИЧР', hover_name='Страна', 
                          color_continuous_scale='Viridis', title='Индекс человеческого развития', 
                          template='plotly_dark')
    ),
# График 4: Страна vs. Население
    dcc.Graph(
        id='population_graph',
        figure=px.scatter(df, x='Страна', y='Население', title='Численность населения стран', 
                          size='Население', color='ИЧР', size_max=60, template='plotly_dark')
    ),

    # График 5: Страна vs. Процент воды
    dcc.Graph(
        id='water_percentage_graph',
        figure=px.pie(df, names='Страна', values='Процент воды в территории', title='Процент воды в странах', 
                      template='plotly_dark')
    ),
       # График 6: Диаграмма рассеяния (ВВП vs. Продолжительность жизни)
    dcc.Graph(
        id='gdp_vs_life_expectancy',
        figure=px.scatter(df, x='ВВП (номинальный, 2024, млрд $)', y='Продолжительность жизни (все)', 
                          title="ВВП vs Продолжительность жизни", 
                          labels={'ВВП (номинальный, 2024, млрд $)': 'ВВП (млрд $)', 'Продолжительность жизни (все)': 'Продолжительность жизни (лет)'},
                          template='plotly_dark')
    ),                                                                   
    # График 7: ВВП по странам
    dcc.Graph(
        id='gdp_graph',
        figure=px.bar(df, x='Страна', y='ВВП (номинальный, 2024, млрд $)', title='Номинальный ВВП стран',
                      color='ВВП (номинальный, 2024, млрд $)', color_continuous_scale='Blues', 
                      template='plotly_dark')
    ),

    # График 8: Продолжительность жизни (мужчины vs женщины)
    dcc.Graph(
        id='life_expectancy_gender_graph',
        figure=px.bar(df, x='Страна', y=['Продолжительность жизни (мужчины)', 'Продолжительность жизни (женщины)'],
                      title='Продолжительность жизни по полу в разных странах', 
                      template='plotly_dark')
    ),
])

# Обновление графиков на основе выбранных стран
@app.callback(
    [Output('area_graph', 'figure'),
     Output('life_expectancy_graph', 'figure')],
    [Input('country_filter', 'value')]
)
def update_graph(selected_countries):
    filtered_df = df[df['Страна'].isin(selected_countries)]
    
    # График 1: Страна vs. Площадь
    area_fig = px.bar(filtered_df, x='Страна', y='Площадь', title='Площадь стран', color='Площадь', 
                      color_continuous_scale='Viridis', template='plotly_dark')
    
    # График 2: Продолжительность жизни по странам
    life_expectancy_fig = px.line(filtered_df, x='Страна', y='Продолжительность жизни (все)', 
                                  title='Продолжительность жизни в разных странах', template='plotly_dark')
    
    return area_fig, life_expectancy_fig

# Запуск сервера
if __name__ == '__main__':
    app.run_server(debug=False)
