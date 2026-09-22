import dash
from dash import html, dcc, callback, Input, Output
import pandas as pd
import sqlite3
import plotly.express as px
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(base_dir)
db_path = os.path.join(parent_dir, 'database.db')

cnx = sqlite3.connect(db_path)
df = pd.read_sql_query('''SELECT * FROM Library_stats''', cnx)
df = df.drop(df[df["Year"] == 2016].index)
df = df.reset_index()
df["date"] = pd.to_datetime(df["Year"].astype(str) + "-" + df["Month"].astype(str))

dash.register_page(__name__,)

layout = html.Div([
    html.H1("Data Visualization", className="text-center my-4"),
    dcc.Dropdown(
        ['Current Loans', 'Library Collections', 'Resources Addded/Catalogued', 'Total Volumes in Library',
         'Website Pageviews', 'Circulation', 'Circulation Transactions',
         'Facilities - no. Of user entering library', 'EZproxy Usage Statistics of E-Resources',
         'Library Floor Area (sq m)', 'Printing/Photocoping Services (Pages)',
         'CityU LibraryFind Homepage (Pageviews)', 'CityUHK Scholars - Work Output',
         'Total No. of Printers/Photocopiers', 'Total No. of Group Study Rooms/Study Carrels',
         'CityUHK Scholars Usage ', 'Total No. of Digital Collections', 'CityUHK Scholars - Records on Portal',
         'Library Instruction Service - Total Participants', 'Library Instruction Service - Total sessions',
         'Enquiries - Total', 'Total No. of Visits', 'Total No. of Visitors',
         'JULAC Cards Issued for CityU Eligible Users for the month', 'No. Of Workshops ',
         'Public Workstations - Total No. of Public Workstations', 'Total No. of Public Workstations',
         'E-Access and Social Media', 'Total No. of Standing Places', 'Digital & Special Collections',
         'Facilities - Seats', 'Total No. of Seats (excluding Standing Places)',
         'Service: Instructions, Enquiries, Events & Visits',
         'Events (Include Live Online Events, Exclude Recorded Events) – Total', 'Total No. of Valid Patrons',
         'Number of Valid Users'],
        ["Current Loans"],
        id='debounce-dropdown',
        debounce=True,
        closeOnSelect=False,
        multi=True,
        maxHeight=600,
        style={'width': '100%', 'minWidth': '400px'}
    ),
    dcc.Graph(id="graph"),
])

@callback(
    Output('graph', 'figure'),
    Input('debounce-dropdown', 'value'),
)
def update_graph(dropdown):
    if not dropdown:
        fig = px.line(title="Please select at least one item from the drop-down menu above to display the chart.")
        return fig

    filtered_df = df[df["DisplayName"].isin(dropdown)]

    fig = px.line(
        filtered_df,
        x="date",
        y="Value",
        color="DisplayName",
        title="Library Statistics Trends",
        labels={"date": "Date", "Value": "Value", "DisplayName": "Metric Component"}
    )

    return fig


