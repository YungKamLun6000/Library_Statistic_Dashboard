from dash import html
import dash_bootstrap_components as dbc


def _column_props(grid_num_setting):
    if grid_num_setting >= 12:
        return {"xs": 12}
    if grid_num_setting <= 3:
        return {"xs": 12, "md": 6, "xl": 4}
    return {"xs": 12, "sm": 6, "xl": 3}


def updated_card(filtered_data, gridNumSetting):
    props = _column_props(gridNumSetting)
    return [
        dbc.Col(
            html.Article(
                [
                    html.P(entry.get("DisplayName", "No Name"), className="metric-label"),
                    html.P(f"{int(entry.get('Value', 0)):,}", className="metric-value"),
                ],
                className="metric-card",
            ),
            className="mb-3",
            **props,
        )
        for entry in filtered_data
    ]
