from dash import Dash, html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import web_api
import pandas as pd

# Import the data from the API
data1 = web_api.Dataapi_import("https://app.lib.cityu.edu.hk/power_bi_api/api/statistics/range?startYear=2025&startMonth=6&endYear=2025&endMonth=6")
data2 = web_api.Dataapi_import_nested("https://app.lib.cityu.edu.hk/power_bi_api/api/statistics/source_path")

Summary_Page_Facts_df = data1[data1["CategoryId"].isin([1])]
Summary_General_df = data1[data1["CategoryId"].isin([2])]
General_Summary_df = data1[data1["CategoryId"].isin([3])]

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

#Components
month_slider = dcc.Slider(1, 12, 1,value=6,id='month')
year_slider = dcc.Slider(2020, 2025, 1,value=2025, id='year')

cards=[
    dbc.Col(
        dbc.Card()
    )]

#layout
app.layout = dbc.Container([
    html.H1("Library Statistics Dashboard", className="text-center my-4"),
    year_slider,
    month_slider,
    dcc.RadioItems(options=['Summary Page - Facts', 'Summary Page for Section Heads', 'General Summary'], value='Summary', id='controls-and-radio-item'),
    dbc.Row(children=cards, className="justify-content-center g-2", id="output_summary")
], fluid=True)

@callback(
    Output(component_id='output_summary', component_property='children'),
    [
        Input(component_id='controls-and-radio-item', component_property='value'),
        Input(component_id='month', component_property='value'),
        Input(component_id='year', component_property='value')
    ]
)

def update_cards(selected_value, month, year):
    if selected_value == 'Summary Page - Facts':
        Summary_Page_Facts_df_filtered_by_year = Summary_Page_Facts_df[Summary_Page_Facts_df["Year"].isin([year])]
        Summary_Page_Facts_df_filtered_by_Month = Summary_Page_Facts_df_filtered_by_year[Summary_Page_Facts_df_filtered_by_year["Month"].isin([month])]
        Summary_Page_Facts = Summary_Page_Facts_df_filtered_by_Month.to_dict(orient="records")
        filtered_data = Summary_Page_Facts
        gridNumSetting = 4
    elif selected_value == 'Summary Page for Section Heads':
        Summary_Page_Facts_df_filtered_by_year = Summary_Page_Facts_df[Summary_Page_Facts_df["Year"].isin([year])]
        Summary_Page_Facts_df_filtered_by_Month = Summary_Page_Facts_df_filtered_by_year[Summary_Page_Facts_df_filtered_by_year["Month"].isin([month])]
        Summary_General = Summary_Page_Facts_df_filtered_by_Month.to_dict(orient="records")
        filtered_data = Summary_General
        gridNumSetting = 3
    else:
        General_Summary_df_filtered_by_year = General_Summary_df[General_Summary_df["Year"].isin([year])]
        General_Summary_df_filtered_by_Month = General_Summary_df_filtered_by_year[General_Summary_df_filtered_by_year["Month"].isin([month])]
        General_Summary = General_Summary_df_filtered_by_Month.to_dict(orient="records")
        filtered_data = General_Summary
        gridNumSetting = 4

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
            width=gridNumSetting,
            className="mb-4",
        )
        for entry in filtered_data
    ]

    return updated_cards


if __name__ == "__main__":
    app.run(debug=True)
