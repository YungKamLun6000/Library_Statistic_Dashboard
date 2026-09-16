import pandas as pd
from dash import Dash, html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import web_api

# Import the data from the API
data1 = web_api.Dataapi_import("https://app.lib.cityu.edu.hk/power_bi_api/api/statistics/range?startYear=2025&startMonth=6&endYear=2025&endMonth=6")
data2 = web_api.Dataapi_import_nested("https://app.lib.cityu.edu.hk/power_bi_api/api/statistics/source_path")
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

Summary_Page_Facts_df = data1[data1["CategoryId"].isin([1])]
Summary_General_df = data1[data1["CategoryId"].isin([2])]
General_Summary = data1[data1["CategoryId"].isin([3])]

# Convert the DataFrame to a list of dictionaries
Summary_Page_Facts_df = Summary_Page_Facts_df.to_dict(orient="records")
Summary_General_df = Summary_General_df.to_dict(orient="records")
General_Summary_df = General_Summary.to_dict(orient="records")

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


cards = [
    dbc.Col(
        dbc.Card(
            dbc.CardBody([
                html.H5(f"{int(entry['Value']):,}", className="card-title text-primary"),  # Format 'Value' with commas
                html.P(entry["DisplayName"], className="card-text"),
            ], className="text-center"),
            style={"border": "1px solid #0d6efd", "borderRadius": "8px"},  # Styling for the card
        ),
        width=4,
        className="mb-4",
    )
    for entry in Summary_Page_Facts_df
]

app.layout = dbc.Container([
    html.H1("Library Statistics Dashboard", className="text-center my-4"),
    dcc.RadioItems(options=['Summary Page - Facts', 'Summary Page for Section Heads', 'General Summary'], value='Summary', id='controls-and-radio-item'),
    dbc.Row(cards, className="justify-content-center g-2", id="output_summary")  # Center the cards
], fluid=True)

@callback(
    Output(component_id='output_summary', component_property='children'),
    Input(component_id='controls-and-radio-item', component_property='value')
)

def update_cards(selected_value):
    if selected_value == 'Summary Page - Facts':
        filtered_data = Summary_Page_Facts_df
        n = 4
    elif selected_value == 'Summary Page for Section Heads':
        filtered_data = Summary_General_df
        n = 3
    else:
        filtered_data = General_Summary_df
        n = 4

    updated_cards = [
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    # Using .get() prevents errors if 'Value' or 'DisplayName' are missing
                    html.H5(f"{int(entry.get('Value', 0)):,}", className="card-title text-primary"),
                    html.P(entry.get("DisplayName", "No Name"), className="card-text"),
                ], className="text-center"),
                style={"border": "1px solid #0d6efd", "borderRadius": "8px"},
            ),
            width=n,
            className="mb-4",
        )
        for entry in filtered_data
    ]

    return updated_cards

if __name__ == "__main__":
    app.run(debug=True)
