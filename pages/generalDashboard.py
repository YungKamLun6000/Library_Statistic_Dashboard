import dash
from dash import Dash, html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import web_api
import Setting_Layout

# Import the data directly from the API
data1 = web_api.Dataapi_import("https://app.lib.cityu.edu.hk/power_bi_api/api/statistics/range?startYear=2015&startMonth=1&endYear=2026&endMonth=12")
data2 = web_api.Dataapi_import_nested("https://app.lib.cityu.edu.hk/power_bi_api/api/statistics/source_path")

Summary_Page_Facts_df = data1[data1["CategoryId"].isin([1])]
Summary_General_df = data1[data1["CategoryId"].isin([2])]
General_Summary_df = data1[data1["CategoryId"].isin([3])]

LibraryInstructionService = ["Library Instruction Service - Total sessions", "Library Instruction Service - Total Participants", "Enquiries - Total", "Events (Include Live Online Events, Exclude Recorded Events) – Total", "Total No. of Visits", "Total No. of Visitors"]
LibraryVisitsbyExternalVisitors = ["Total No. of Visits", "Total No. of Visitors"]

dash.register_page(__name__, path="/")

#Components
month_slider = dcc.Dropdown(
    [i for i in range(1, 13)] ,
    [6],
    debounce=True,
    multi=True,
    id='month'
)

year_slider = dcc.Dropdown(
    [i for i in range(2016, 2027)] ,
    [2025],
    debounce=True,
    multi=True,
    id ='year'
)

cards=[
    dbc.Col(
        dbc.Card()
    )]

#layout
layout = dbc.Container([
    html.H1("General Dashboard", className="text-center my-4"),
    year_slider,
    month_slider,
    dcc.RadioItems(options=['Summary Page - Facts', 'Summary Page for Section Heads', 'General Summary','Library Instruction Service'], value='General Summary', id='controls-and-radio-item'),
    html.Div(id='output_summary'),
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
    if not month or not year:
        return html.Div("Please select at least one Year and Month.", className="text-center my-4 text-danger")

    if selected_value == 'Summary Page - Facts':
        Summary_Page_Facts_df_filtered_by_year = Summary_Page_Facts_df[Summary_Page_Facts_df["Year"].isin(year)]
        Summary_Page_Facts_df_filtered_by_Month = Summary_Page_Facts_df_filtered_by_year[Summary_Page_Facts_df_filtered_by_year["Month"].isin(month)]
        Summary_Page_Facts_df_filtered_by_Month = Summary_Page_Facts_df_filtered_by_Month.groupby('DisplayName', as_index=False).agg('sum')
        Summary_Page_Facts = Summary_Page_Facts_df_filtered_by_Month.to_dict(orient="records")
        filtered_data = Summary_Page_Facts

        gridNumSetting = 4
        cards = Setting_Layout.updated_card(filtered_data, gridNumSetting)
    elif selected_value == 'Summary Page for Section Heads':
        Summary_Page_Facts_df_filtered_by_year = Summary_Page_Facts_df[Summary_Page_Facts_df["Year"].isin(year)]
        Summary_Page_Facts_df_filtered_by_Month = Summary_Page_Facts_df_filtered_by_year[Summary_Page_Facts_df_filtered_by_year["Month"].isin(month)]
        Summary_Page_Facts_df_filtered_by_Month = Summary_Page_Facts_df_filtered_by_Month.groupby('DisplayName', as_index=False).agg('sum')
        Summary_General = Summary_Page_Facts_df_filtered_by_Month.to_dict(orient="records")
        filtered_data = Summary_General

        gridNumSetting = 3
        cards = Setting_Layout.updated_card(filtered_data, gridNumSetting)
    elif selected_value == 'General Summary':
        General_Summary_df_filtered_by_year = General_Summary_df[General_Summary_df["Year"].isin(year)]
        General_Summary_df_filtered_by_Month = General_Summary_df_filtered_by_year[General_Summary_df_filtered_by_year["Month"].isin(month)]
        General_Summary_df_filtered_by_Month = General_Summary_df_filtered_by_Month[~General_Summary_df_filtered_by_Month["DisplayName"].isin(LibraryInstructionService)]
        General_Summary_df_filtered_by_Month = General_Summary_df_filtered_by_Month.groupby('DisplayName', as_index=False).agg('sum')
        General_Summary = General_Summary_df_filtered_by_Month.to_dict(orient="records")
        filtered_data = General_Summary

        gridNumSetting = 4
        cards = Setting_Layout.updated_card(filtered_data, gridNumSetting)
    else:
        General_Summary_df_filtered_by_year = General_Summary_df[General_Summary_df["Year"].isin(year)]
        General_Summary_df_filtered_by_Month = General_Summary_df_filtered_by_year[General_Summary_df_filtered_by_year["Month"].isin(month)]
        General_Summary_df_filtered_by_Month = General_Summary_df_filtered_by_Month[General_Summary_df_filtered_by_Month["DisplayName"].isin(LibraryInstructionService)]

        General_Summary_df_filtered_by_Month = General_Summary_df_filtered_by_Month.groupby('DisplayName', as_index=False).agg('sum')

        Vistors_df = General_Summary_df_filtered_by_Month[General_Summary_df_filtered_by_Month["DisplayName"].isin(LibraryVisitsbyExternalVisitors)]
        Library_df = General_Summary_df_filtered_by_Month[~General_Summary_df_filtered_by_Month["DisplayName"].isin(LibraryVisitsbyExternalVisitors)]

        Vistors_data = Vistors_df.to_dict(orient="records")
        Library_data = Library_df.to_dict(orient="records")

        gridNumSetting = 12
        Vistors_cards = Setting_Layout.updated_card(Vistors_data, gridNumSetting)
        Library_cards = Setting_Layout.updated_card(Library_data, gridNumSetting)

        layout = [
            dbc.Row(
                children=[
                    dbc.Col(
                        children=[
                            html.H4("Library Instruction Service", className="text-center mb-3 fw-bold"),
                            dbc.Row(children=Library_cards, className="justify-content-center g-2",
                                    id="library_summary")
                        ],
                        width=6
                    ),

                    dbc.Col(
                        children=[
                            html.H4("Library Visits by External Visitors", className="text-center mb-3 fw-bold"),
                            dbc.Row(children=Vistors_cards, className="justify-content-center g-2",
                                    id="visitors_summary")
                        ],
                        width=6
                    )
                ],
                className="g-4"
            )
        ]

        return layout

    layout = [dbc.Row(children=cards, className="justify-content-center g-2")]
    return layout