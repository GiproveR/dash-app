from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import os

df = pd.read_csv('gapminder_unfiltered.csv')

assets_dir = os.path.join(os.path.dirname(__file__), 'assets')
engine_path = os.path.join(assets_dir, 'engine.txt')

with open(engine_path, 'r', encoding='utf-8') as f:
    plotly_js_code = f.read()

app = Dash()

app.scripts.config.serve_locally = True
app.css.config.serve_locally = True

app.index_string = f'''
<!DOCTYPE html>
<html>
    <head>
        {{%metas%}}
        <title>{{%title%}}</title>
        {{%favicon%}}
        {{%css%}}
    </head>
    <body>
        {{%app_entry%}}
        <footer>
            {{%config%}}
            <script>{plotly_js_code}</script>
            {{%scripts%}}
            {{%renderer%}}
        </footer>
    </body>
</html>
'''

app.scripts.js_modules = [
    module for module in app.scripts.get_all_scripts() 
    if module['package_name'] != 'dash' or 'plotly' not in module.get('dev_package_path', '')
]

server = app.server

custom_dropdown_options = [
    {'label': 'Country', 'value': 'country'},
    {'label': 'Continent', 'value': 'continent'},
    {'label': 'Year', 'value': 'year'},
    {'label': 'Life expectancy', 'value': 'lifeExp'},
    {'label': 'Population', 'value': 'pop'},
    {'label': 'GDP per cap', 'value': 'gdpPercap'}
]

numeric_dropdown_options = [
    {'label': 'Life expectancy', 'value': 'lifeExp'},
    {'label': 'Population', 'value': 'pop'},
    {'label': 'GDP per cap', 'value': 'gdpPercap'}
]

app.layout = html.Div(
    style={
        'backgroundColor': '#f8f9fa', 
        'fontFamily': '"Segoe UI", Roboto, Helvetica, Arial, sans-serif', 
        'padding': '30px 40px', 
        'minHeight': '100vh'
    },
    children=[
        html.Div(
            style={'maxWidth': '1400px', 'margin': '0 auto', 'display': 'flex', 'flexDirection': 'column', 'gap': '30px'},
            children=[
                
                html.Div(
                    style={
                        'display': 'flex', 
                        'flexDirection': 'row', 
                        'alignItems': 'center', 
                        'flexWrap': 'wrap',
                        'gap': '15px', 
                        'marginBottom': '10px'
                    },
                    children=[
                        html.H1(
                            'Dashboard of world population on', 
                            style={'margin': '0', 'color': '#2c3e50', 'fontWeight': '600', 'fontSize': '32px', 'lineHeight': '1'}
                        ),
                        html.Div(
                            dcc.Dropdown(
                                options=df.year.unique(), 
                                value=1999, 
                                id='year-selection',
                                clearable=False,
                                style={'border': 'none', 'backgroundColor': 'transparent'}
                            ),
                            style={'width': '120px', 'fontSize': '28px', 'fontWeight': '600', 'color': '#3498db'}
                        ),
                    ]
                ),

                html.Div(
                    style={'display': 'flex', 'flexDirection': 'row', 'gap': '25px', 'flexWrap': 'wrap'},
                    children=[
                        html.Div(
                            style={'flex': '1.5', 'minWidth': '550px', 'backgroundColor': '#ffffff', 'borderRadius': '16px', 'padding': '25px', 'boxShadow': '0 4px 20px rgba(0,0,0,0.04)', 'display': 'flex', 'flexDirection': 'column', 'gap': '20px'},
                            children=[
                                html.H4('Population in countries', style={'margin': '0', 'color': '#34495e', 'fontSize': '18px'}),
                                html.Div(
                                    style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '15px'},
                                    children=[
                                        html.Div([
                                            html.Label('Select Countries:', style={'fontSize': '13px', 'fontWeight': '500', 'color': '#7f8c8d', 'marginBottom': '6px', 'display': 'block'}), 
                                            dcc.Dropdown(df.country.unique(), ['Canada'], id='dropdown-selection', multi=True)
                                        ]),
                                        html.Div([
                                            html.Label('Y-Axis Metric:', style={'fontSize': '13px', 'fontWeight': '500', 'color': '#7f8c8d', 'marginBottom': '6px', 'display': 'block'}), 
                                            dcc.Dropdown(options=numeric_dropdown_options, value='pop', id='linear-axis-y')
                                        ]),
                                    ]
                                ),
                                dcc.Graph(id='linear-graph', style={'flex': '1'})
                            ]
                        ),
                        
                        html.Div(
                            style={'flex': '1', 'minWidth': '350px', 'backgroundColor': '#ffffff', 'borderRadius': '16px', 'padding': '25px', 'boxShadow': '0 4px 20px rgba(0,0,0,0.04)', 'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'},
                            children=[
                                html.H4('Top 15-countries with biggest population', style={'margin': '0', 'color': '#34495e', 'fontSize': '18px'}),
                                dcc.Graph(id='bar-graph', style={'width': '100%'}), 
                            ]
                        ),
                    ]
                ),

                html.Div(
                    style={'display': 'flex', 'flexDirection': 'row', 'gap': '25px', 'flexWrap': 'wrap'},
                    children=[
                        html.Div(
                            style={'flex': '1.5', 'minWidth': '550px', 'backgroundColor': '#ffffff', 'borderRadius': '16px', 'padding': '25px', 'boxShadow': '0 4px 20px rgba(0,0,0,0.04)', 'display': 'flex', 'flexDirection': 'column', 'gap': '20px'},
                            children=[
                                html.H4('Custom graph', style={'margin': '0', 'color': '#34495e', 'fontSize': '18px'}),
                                html.Div(
                                    style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr 1fr', 'gap': '12px'},
                                    children=[
                                        html.Div([html.Label('X Axis', style={'fontSize': '12px', 'color': '#7f8c8d', 'fontWeight': '500'}), dcc.Dropdown(options=custom_dropdown_options, value='country', id='scatter-x-dropdown')]),
                                        html.Div([html.Label('Y Axis', style={'fontSize': '12px', 'color': '#7f8c8d', 'fontWeight': '500'}), dcc.Dropdown(options=custom_dropdown_options, value='lifeExp', id='scatter-y-dropdown')]),
                                        html.Div([html.Label('Radius', style={'fontSize': '12px', 'color': '#7f8c8d', 'fontWeight': '500'}), dcc.Dropdown(options=custom_dropdown_options, value='pop', id='scatter-r-dropdown')]),
                                    ]
                                ),
                                dcc.Graph(id='scatter-graph', style={'flex': '1'})
                            ]
                        ),
                        
                        html.Div(
                            style={'flex': '1', 'minWidth': '350px', 'backgroundColor': '#ffffff', 'borderRadius': '16px', 'padding': '25px', 'boxShadow': '0 4px 20px rgba(0,0,0,0.04)', 'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'},
                            children=[
                                html.H4('Population on continents', style={'margin': '0', 'color': '#34495e', 'fontSize': '18px'}),
                                dcc.Graph(id='pie-graph', style={'width': '100%'}),
                            ]
                        ),
                    ]
                ),
            ]
        )
    ]
)

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
        #orientation='h'
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