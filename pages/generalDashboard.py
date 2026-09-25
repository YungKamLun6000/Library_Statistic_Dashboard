import dash
from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import web_api
import Setting_Layout

DATA_URL = (
    "https://app.lib.cityu.edu.hk/power_bi_api/api/statistics/range"
    "?startYear=2015&startMonth=1&endYear=2026&endMonth=12"
)

load_error = None
try:
    data1 = web_api.Dataapi_import(DATA_URL)
except Exception as exc:
    data1 = None
    load_error = str(exc)

if data1 is not None:
    Summary_Page_Facts_df = data1[data1["CategoryId"].isin([1])]
    Summary_General_df = data1[data1["CategoryId"].isin([2])]
    General_Summary_df = data1[data1["CategoryId"].isin([3])]
else:
    Summary_Page_Facts_df = Summary_General_df = General_Summary_df = None

LibraryInstructionService = [
    "Library Instruction Service - Total sessions",
    "Library Instruction Service - Total Participants",
    "Enquiries - Total",
    "Events (Include Live Online Events, Exclude Recorded Events) – Total",
    "Total No. of Visits",
    "Total No. of Visitors",
]
LibraryVisitsbyExternalVisitors = ["Total No. of Visits", "Total No. of Visitors"]

dash.register_page(__name__, path="/", name="General Dashboard", order=0)

MONTHS = [
    {"label": name, "value": index}
    for index, name in enumerate(
        ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
        start=1,
    )
]

year_slider = dcc.Dropdown(
    list(range(2016, 2027)),
    [2025],
    debounce=True,
    multi=True,
    id="year",
    placeholder="Select years",
    className="filter-dropdown",
)

month_slider = dcc.Dropdown(
    MONTHS,
    [6],
    debounce=True,
    multi=True,
    id="month",
    placeholder="Select months",
    className="filter-dropdown",
)

layout = html.Div(
    [
        html.Header(html.H1("General Dashboard"), className="page-head"),
        html.Section(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [html.Label("Year", className="field-label"), year_slider],
                            md=6,
                            className="mb-3",
                        ),
                        dbc.Col(
                            [html.Label("Month", className="field-label"), month_slider],
                            md=6,
                            className="mb-3",
                        ),
                    ]
                ),
                html.Label("Report", className="field-label"),
                dcc.RadioItems(
                    options=[
                        "Summary Page - Facts",
                        "Summary Page for Section Heads",
                        "General Summary",
                        "Library Instruction Service",
                    ],
                    value="General Summary",
                    id="controls-and-radio-item",
                    className="view-switch",
                ),
            ],
            className="panel",
        ),
        dcc.Loading(
            html.Div(id="output_summary"),
            type="dot",
            color="#c41230",
        ),
    ]
)


def _cards_for(frame, grid):
    grouped = frame.groupby("DisplayName", as_index=False)["Value"].sum()
    records = grouped.to_dict(orient="records")
    return records, Setting_Layout.updated_card(records, grid)


@callback(
    Output("output_summary", "children"),
    Input("controls-and-radio-item", "value"),
    Input("month", "value"),
    Input("year", "value"),
)
def update_cards(selected_value, month, year):
    if load_error or General_Summary_df is None:
        return html.Div(
            "The statistics service did not respond. Refresh the page once the library API is reachable.",
            className="alert-banner",
        )

    if not month or not year:
        return html.Div("Select at least one year and one month.", className="empty-note")

    if selected_value == "Summary Page - Facts":
        frame = Summary_Page_Facts_df
        grid = 4
    elif selected_value == "Summary Page for Section Heads":
        frame = Summary_General_df
        grid = 3
    elif selected_value == "General Summary":
        frame = General_Summary_df[~General_Summary_df["DisplayName"].isin(LibraryInstructionService)]
        grid = 4
    else:
        frame = General_Summary_df[
            General_Summary_df["Year"].isin(year) & General_Summary_df["Month"].isin(month)
        ]
        frame = frame[frame["DisplayName"].isin(LibraryInstructionService)]
        grouped = frame.groupby("DisplayName", as_index=False)["Value"].sum()
        visitors = grouped[grouped["DisplayName"].isin(LibraryVisitsbyExternalVisitors)]
        instruction = grouped[~grouped["DisplayName"].isin(LibraryVisitsbyExternalVisitors)]
        visitor_cards = Setting_Layout.updated_card(visitors.to_dict(orient="records"), 12)
        instruction_cards = Setting_Layout.updated_card(instruction.to_dict(orient="records"), 12)
        return html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            html.Section(
                                [
                                    html.H2("Library Instruction Service", className="panel-title"),
                                    dbc.Row(instruction_cards, className="g-3"),
                                ],
                                className="split-panel",
                            ),
                            lg=6,
                            className="mb-3",
                        ),
                        dbc.Col(
                            html.Section(
                                [
                                    html.H2("Library Visits by External Visitors", className="panel-title"),
                                    dbc.Row(visitor_cards, className="g-3"),
                                ],
                                className="split-panel",
                            ),
                            lg=6,
                            className="mb-3",
                        ),
                    ],
                    className="g-3",
                ),
            ]
        )

    filtered = frame[frame["Year"].isin(year) & frame["Month"].isin(month)]
    records, cards = _cards_for(filtered, grid)
    if not records:
        return html.Div("No figures match this report and period.", className="empty-note")

    return dbc.Row(cards, className="g-2")
