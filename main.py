from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')
print(df.info())

app = Dash()

columns_names = list(df.columns.values)
numeric_column_names = list(df.select_dtypes((int, float)).columns.values)
numeric_column_names.remove('year')

app.layout = [
    html.H1(children='Title of Dash App', style={'textAlign':'center'}),
    dcc.Dropdown(df.country.unique(), ['Canada'], id='dropdown-selection', multi=True),
    dcc.Dropdown(numeric_column_names, 'pop', id='linear-axis-y'),
    dcc.Dropdown(df.year.unique(), 1999, id='year-selection'),
    dcc.Graph(id='linear-graph'),
    dcc.Graph(id='bar-graph'),
    dcc.Graph(id='pie-graph'),
    dcc.Dropdown(columns_names, 'country', id='scatter-x-dropdown'),
    dcc.Dropdown(columns_names, 'lifeExp', id='scatter-y-dropdown'),
    dcc.Dropdown(columns_names, 'pop', id='scatter-r-dropdown'),
    dcc.Graph(id='scatter-graph')
]

@callback(
    Output('linear-graph', 'figure'),
    Input('dropdown-selection', 'value'),
    Input('linear-axis-y', 'value')
)
def linear_graph(value, axisY):
    dff = df[df.country.isin(value)]
    return px.line(dff, x='year', y=axisY, color='country')

@callback(
    Output('bar-graph', 'figure'),
    Input('year-selection', 'value')
)
def top15_countries(value):
    dff = df[['pop', 'country']][df.year == value].sort_values(by='pop', ascending=False).head(15)
    fig = px.bar(
        dff,
        x='pop',
        y='country',
        #orientation='h',
        title='Top 15-countries with biggest population'
    )
    fig.update_yaxes(autorange="reversed")
    return fig

@callback(
    Output('pie-graph', 'figure'),
    Input('year-selection', 'value')
)
def pie_graph(value):
    dff = df[['pop', 'continent']][df.year == value].groupby(by='continent', as_index=False).sum()
    return px.pie(dff, values='pop', names='continent')

@callback(
    Output('scatter-graph', 'figure'),
    Input('scatter-x-dropdown', 'value'),
    Input('scatter-y-dropdown', 'value'),
    Input('scatter-r-dropdown', 'value'),
    Input('year-selection', 'value')
)
def scatter_graph(valueX, valueY, valueR, year):
    dff = df[df.year == year]
    return px.scatter(dff, x=valueX, y=valueY, size=valueR)

if __name__ == '__main__':
    app.run(debug=True)