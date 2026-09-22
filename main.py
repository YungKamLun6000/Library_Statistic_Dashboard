import dash
from dash import Dash, html
import dash_bootstrap_components as dbc

app = Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.FLATLY, dbc.icons.BOOTSTRAP],
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}]
)

nav_links = [
    dbc.NavItem(
        dbc.NavLink(
            page["name"],
            href=page["relative_path"],
            active="exact",
            className="px-3 py-2 rounded text-black fw-bold text-decoration-none"
        )
    )
    for page in dash.page_registry.values()
]

app.layout = html.Div([
    dbc.Navbar(
        dbc.Container([

            dbc.NavbarBrand(
                html.Span([
                    html.Img(
                        src=app.get_asset_url("CityUicon.png"),
                        style={"height": "32px", "object-fit": "contain"},
                        className="me-3"
                    ),
                    "Library Analytics Portal"
                ], className="d-flex align-items-center"),
                href="#",
                className="text-black fw-bold text-decoration-none"
            ),

            dbc.Nav(
                nav_links,
                navbar=True,
                className="ms-auto d-flex flex-row align-items-center"
            )

        ], fluid=True, className="px-4"),
        dark=False,
        sticky="top",
        className="border-bottom shadow-sm mb-4 py-3",
        style={
            "background": "linear-gradient(90deg, #db8a8a 0%, #f03232 30%, #f21616 70%, #ff0000 100%)",
            "border": "none"
        }
    ),

    dbc.Container([
        html.Main([
            dash.page_container
        ], className="bg-white p-4 rounded-3 shadow-sm min-vh-75")
    ], fluid=True, className="px-md-5 pb-5")
], className="bg-light min-vh-100")

if __name__ == "__main__":
    app.run(debug=False)
