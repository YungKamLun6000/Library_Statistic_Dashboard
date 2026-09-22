import os
import sqlite3
import pandas as pd
from dash import html, Input, Output, callback, State, dash_table
import dash_bootstrap_components as dbc
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import dash
import re


# Define repository and model path
MODEL_NAME = "Qwen/Qwen2.5-Coder-1.5B-Instruct"  # Replace colon with valid character!

# Check Hugging Face Token
os.environ["HF_TOKEN"] = "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"  # Set your Hugging Face token

base_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(base_dir)
db_path = os.path.join(parent_dir, 'database.db')

print("Loading model and tokenizer locally...")
try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, token=os.environ["HF_TOKEN"])
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        token=os.environ["HF_TOKEN"],
        torch_dtype="auto",
        device_map="auto"
    )
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

    input_text = f"only include SQL string(Table name is Library_stats): {value}"
    print(f"User Request: {input_text}")

    inputs = tokenizer(input_text, return_tensors="pt").to(device)

    outputs = model.generate(**inputs, max_length=100, num_return_sequences=1)
    full_output = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
    print(f"Full Model Output: {full_output}")

    sql_match = re.search(r'(SELECT[\s\S]*?;)', full_output, re.IGNORECASE)

    if sql_match:
        sql_query = sql_match.group(1).strip()
    else:
        sql_match_backup = re.search(r'(SELECT[\s\S]*)', full_output, re.IGNORECASE)
        sql_query = sql_match_backup.group(1).strip() if sql_match_backup else full_output

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

