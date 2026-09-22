import os
import sqlite3
import pandas as pd
from dash import html, Input, Output, callback, State
import dash_bootstrap_components as dbc
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import dash
import re


base_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(base_dir)
path = os.path.join(parent_dir, "models")

base_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(base_dir)
db_path = os.path.join(parent_dir, 'database.db')

print("Loading model and tokenizer locally...")
try:
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(device)
    model = AutoModelForCausalLM.from_pretrained(path, local_files_only=True)
    tokenizer = AutoTokenizer.from_pretrained(path, local_files_only=True)
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    exit()

dash.register_page(
    __name__,
    path="/natural-language-query",
    name="Natural Language Query",
)

layout = html.Div([
    dbc.Input(id="input", placeholder="Type a query...", type="text"),
    dbc.Button("Submit", id="submit-btn", color="primary", className="mt-2"),
    html.Br(),
    html.Div(id="output")
])

@callback(
    Output("output", "children"),
    [Input("submit-btn", "n_clicks"),
     Input("input", "n_submit")],
    State("input", "value"),
    prevent_initial_call=True
)
def update_output(n_clicks, n_submit, value):
    if not value or (n_clicks is None and n_submit is None):
        return "Please type a query and click Submit or press Enter."

    SYSTEM_PROMPT = """You are a strict SQL generator. Your only job is to convert natural language into a valid SQL query based on the following database schema.

    Table Name: Library_stats
    Columns:
    - Year (INT): The year of the record (e.g., 2016, 2017)
    - Month (INT): The month of the record (e.g., 6, 7)
    - Display_Name (VARCHAR): The metric or facility name (e.g., 'Facilities...', 'Total Number...', 'Library Funding...')
    - Value (FLOAT): The numerical value or count for the metric
    - Frequency (VARCHAR): Frequency of data collection (e.g., 'M' for Monthly)
    - Cumulative_Type (VARCHAR): Type of accumulation (e.g., 'c', 'i')
    - Category_Id_1 (INT): Classification category ID
    - Category_Id_2 (INT): Secondary classification category ID
    - Display_Order (INT): The order for display purposes
    """

    input_text = f"{SYSTEM_PROMPT} only return the SQL query in one sentence, Question: {value}"
    print(f"User Request: {input_text}")

    inputs = tokenizer(input_text, return_tensors="pt").to(device)
    input_length = inputs.input_ids.shape[1]

    outputs = model.generate(**inputs, max_length=100000, num_return_sequences=1)
    full_output = tokenizer.decode(outputs[0][input_length:], skip_special_tokens=True).strip()
    print(f"Full Model Output: {full_output}")

    sql_match = re.search(r'(SELECT[^;]*?;)', full_output, re.IGNORECASE)

    if sql_match:
        sql_query = sql_match.group(1).strip()
    else:
        sql_match_backup = re.search(r'(SELECT[\s\S]*)', full_output, re.IGNORECASE)
        sql_query = sql_match_backup.group(1).strip() if sql_match_backup else full_output
        sql_query = re.sub(r'```.*$', '', sql_query, flags=re.DOTALL).strip()

    print(f"Extracted SQL query: {sql_query}")

    try:
        with sqlite3.connect(db_path) as current_cnx:
            df = pd.read_sql_query(sql_query, current_cnx)

        return html.Div([
            html.H4("Query Results:"),
            html.Iframe(
                srcDoc=df.to_html(index=False, classes='table table-striped table-hover', escape=False),
                style={"width": "100%", "height": "400px", "border": "none"}
            )
        ])

    except Exception as err:
        return html.Div([
            html.H4("Error executing SQL query:"),
            html.P(str(err), style={"color": "red"})
        ])

