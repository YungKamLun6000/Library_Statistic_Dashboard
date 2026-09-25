# CityU Library Analytics

A Dash dashboard for City University of Hong Kong library statistics. The overview page totals live figures from the library API. The trends page charts the local SQLite copy.

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

Open [http://127.0.0.1:8741](http://127.0.0.1:8741).

`API_Grabber_to_database.py` refreshes `database.db` from the same statistics service.
