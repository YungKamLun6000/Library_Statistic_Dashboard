from dash import html
import dash_bootstrap_components as dbc

def updated_card(filtered_data, gridNumSetting):
    updated_cards = [
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
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