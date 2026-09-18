import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

#layout
app.layout = dbc.Container([
    html.H1("Library Statistics", className="text-center my-4"),
    html.Div([
        html.Div(
            dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"])
        ) for page in dash.page_registry.values()
    ]),
    dash.page_container
], fluid=True)

if __name__ == "__main__":
    app.run(debug=True)
