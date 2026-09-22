"""
import os
from huggingface_hub import InferenceClient
import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import sqlite3

os.environ["HF_TOKEN"] = "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"

client = InferenceClient(
    api_key=os.environ["HF_TOKEN"],
)

base_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(base_dir)
db_path = os.path.join(parent_dir, 'database.db')

cnx = sqlite3.connect(db_path)

dash.register_page(__name__,path="/natural-language-query", name="Natural Language Query",)

layout = html.Div(
    [
        dbc.Input(id="input", placeholder="Type something...", type="text"),
        html.Br(),
        html.P(id="output"),

    ]
)

@callback(Output("output", "children"), [Input("input", "value")])

def update_output(value):
    if not value:
        return "Please type a query to generate results."

    completion = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-V4.1-Flash:fireworks-ai",
        messages=[
            {
                "role": "system",
                "content": "Output nothing but a SQL query string"
            },
            {
                "role": "user",
                "content": str(value)
            }
        ],
    )

    sql_query = completion.choices[0].message.content.strip()

    try:
        df = pd.read_sql_query(sql_query, cnx)

        return html.Div([
            html.H4("Query Results:"),
            html.Div(
                df.to_html(index=False, classes='table table-striped table-hover', escape=False),
                style={"overflowX": "auto"},
            )
        ])
    except Exception as e:
        return f"Error executing query: {str(e)}"

"""