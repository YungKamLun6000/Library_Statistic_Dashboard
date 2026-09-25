import os
import sqlite3

import dash
import pandas as pd
import plotly.express as px
from dash import html, dcc, callback, Input, Output

base_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(base_dir)
db_path = os.path.join(parent_dir, "database.db")

load_error = None
df = pd.DataFrame()
try:
    with sqlite3.connect(db_path) as cnx:
        df = pd.read_sql_query("SELECT * FROM Library_stats", cnx)
    df = df.drop(df[df["Year"] == 2016].index)
    df = df.reset_index(drop=True)
    df["date"] = pd.to_datetime(df["Year"].astype(str) + "-" + df["Month"].astype(str))
except Exception as exc:
    load_error = str(exc)

METRICS = [
    "Current Loans",
    "Library Collections",
    "Resources Addded/Catalogued",
    "Total Volumes in Library",
    "Website Pageviews",
    "Circulation",
    "Circulation Transactions",
    "Facilities - no. Of user entering library",
    "EZproxy Usage Statistics of E-Resources",
    "Library Floor Area (sq m)",
    "Printing/Photocoping Services (Pages)",
    "CityU LibraryFind Homepage (Pageviews)",
    "CityUHK Scholars - Work Output",
    "Total No. of Printers/Photocopiers",
    "Total No. of Group Study Rooms/Study Carrels",
    "CityUHK Scholars Usage ",
    "Total No. of Digital Collections",
    "CityUHK Scholars - Records on Portal",
    "Library Instruction Service - Total Participants",
    "Library Instruction Service - Total sessions",
    "Enquiries - Total",
    "Total No. of Visits",
    "Total No. of Visitors",
    "JULAC Cards Issued for CityU Eligible Users for the month",
    "No. Of Workshops ",
    "Public Workstations - Total No. of Public Workstations",
    "Total No. of Public Workstations",
    "E-Access and Social Media",
    "Total No. of Standing Places",
    "Digital & Special Collections",
    "Facilities - Seats",
    "Total No. of Seats (excluding Standing Places)",
    "Service: Instructions, Enquiries, Events & Visits",
    "Events (Include Live Online Events, Exclude Recorded Events) – Total",
    "Total No. of Valid Patrons",
    "Number of Valid Users",
]

COLORWAY = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f"]

dash.register_page(__name__, name="Data Visualization", order=1, path="/visualizations")

layout = html.Div(
    [
        html.Header(
            [
                html.H1("Data Visualization"),
                html.P("Pick one series or several.", className="lede"),
            ],
            className="page-head",
        ),
        html.Section(
            [
                html.Label("Metrics", className="field-label"),
                dcc.Dropdown(
                    METRICS,
                    ["Current Loans"],
                    id="debounce-dropdown",
                    debounce=True,
                    closeOnSelect=False,
                    multi=True,
                    maxHeight=420,
                    placeholder="Choose metrics",
                    className="filter-dropdown",
                ),
            ],
            className="panel",
        ),
        html.Section(
            dcc.Loading(
                dcc.Graph(
                    id="graph",
                    className="chart-frame",
                    config={"displayModeBar": False, "responsive": True},
                ),
                type="dot",
                color="#c41230",
            ),
            className="panel",
        ),
    ]
)


def _style_figure(fig):
    fig.update_layout(
        template="plotly_white",
        font={"family": "system-ui, Segoe UI, Roboto, Helvetica, Arial, sans-serif", "color": "#1a1a1a", "size": 12},
        title={"font": {"family": "system-ui, Segoe UI, Roboto, Helvetica, Arial, sans-serif", "size": 16, "color": "#111"}, "x": 0.01},
        legend={"orientation": "h", "yanchor": "top", "y": -0.2, "x": 0},
        margin={"l": 40, "r": 16, "t": 40, "b": 40},
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        colorway=COLORWAY,
    )
    fig.update_xaxes(showgrid=False, linecolor="#e5e7eb", tickfont={"size": 11})
    fig.update_yaxes(gridcolor="#f0f0f0", zeroline=False, linecolor="#e5e7eb", tickfont={"size": 11})
    fig.update_traces(line={"width": 2})
    return fig


@callback(
    Output("graph", "figure"),
    Input("debounce-dropdown", "value"),
)
def update_graph(dropdown):
    if load_error:
        fig = px.line(title="The local statistics database could not be opened.")
        return _style_figure(fig)

    if not dropdown:
        fig = px.line(title="Select at least one metric to draw the chart.")
        return _style_figure(fig)

    filtered_df = df[df["DisplayName"].isin(dropdown)]
    fig = px.line(
        filtered_df,
        x="date",
        y="Value",
        color="DisplayName",
        title="Library statistics trends",
        labels={"date": "Date", "Value": "Value", "DisplayName": "Metric"},
    )
    return _style_figure(fig)
