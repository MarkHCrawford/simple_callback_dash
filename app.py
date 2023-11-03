import pandas as pd
from dash import Dash, Input, Output, dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import requests

response = requests.get("https://data.ny.gov/resource/487n-fp4r.json")
df = pd.DataFrame(response.json())

df.dropna(inplace=True)
df = df[df["enrollment_type_description"] == 'Total']

# Includes bootstrap theme from an online stylesheet
app = Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.FLATLY])


# Layout using Dash HTML components
app.layout = html.Div([
    html.H1("CUNY Data", style={'text-align': 'center'}),
    
    # Dropdown menu to select the year
    dcc.Dropdown(
        id='fall-term-dropdown',
        options=[{'label': year, 'value': year} for year in df['fall_term'].unique()],
        value=2007  # Set the default year to 2007
    ),
    
    # Histogram plot
    dcc.Graph(id='college-histogram'),

    
])

# Define a callback to update the histogram and the average number of students enrolled
@app.callback(
    # Output list for multiple outputs
    Output('college-histogram', 'figure'),
    # Input from year dropdown
    Input('fall-term-dropdown', 'value')
)
def update_histogram(selected_year):
    # Change dataframe with the selected year
    filtered_df = df[df['fall_term'] == selected_year]
    # Plotly Histogram
    fig = px.histogram(filtered_df, x='college_name', y='head_count', title=f"College Data for {selected_year}")
    # Change names of the Axes
    fig.update_xaxes(title_text="College Name")
    fig.update_yaxes(title_text="Head Count")
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
