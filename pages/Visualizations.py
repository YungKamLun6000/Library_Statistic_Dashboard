import dash
from dash import html
dash.register_page(__name__,)

layout = html.Div([
    html.H1("Visualization", className="text-center my-4"),
])
