import dash
from dash import Dash, Input, Output, State, html
import dash_bootstrap_components as dbc

app = Dash(
    __name__,
    use_pages=True,
    title="CityU Library Analytics",
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        dbc.icons.BOOTSTRAP,
    ],
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)

nav_links = [
    dbc.NavItem(
        dbc.NavLink(
            page["name"],
            href=page["relative_path"],
            active="exact",
        )
    )
    for page in sorted(dash.page_registry.values(), key=lambda page: page["order"])
]

app.layout = html.Div(
    [
        dbc.Navbar(
            dbc.Container(
                [
                    html.A(
                        [
                            html.Img(
                                src=app.get_asset_url("CityUicon.png"),
                                className="brand-mark",
                                alt="City University of Hong Kong",
                            ),
                            html.Span(
                                [
                                    html.Span("CityU Library", className="brand-kicker"),
                                    html.Span("Analytics", className="brand-title"),
                                ]
                            ),
                        ],
                        href="/",
                        className="brand-lockup",
                    ),
                    dbc.NavbarToggler(id="nav-toggler", n_clicks=0),
                    dbc.Collapse(
                        dbc.Nav(nav_links, navbar=True, className="ms-lg-auto nav-pills-modern"),
                        id="nav-collapse",
                        is_open=False,
                        navbar=True,
                    ),
                ],
                fluid=True,
                className="px-3 px-lg-4",
            ),
            sticky="top",
            expand="lg",
            color="danger",
            dark=True,
            className="app-nav",
        ),
        html.Main(dash.page_container, className="app-main"),
    ],
    className="app-shell",
)


@app.callback(
    Output("nav-collapse", "is_open"),
    Input("nav-toggler", "n_clicks"),
    State("nav-collapse", "is_open"),
)
def toggle_nav(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8741)
