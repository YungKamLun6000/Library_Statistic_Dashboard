# Library Statistics Dashboard

This project is a **Library Statistics Dashboard** built using Python and Dash to provide data visualizations and general statistics on a simple, interactive dashboard.

---

## Features

- **Data Visualizations**: Time-series plots and other insights generated from the library database.
- **General Dashboard**: Displays key statistics and metrics for the library.

---

## Requirements

### Software Requirements:

1. **Python Version**: Python 3.14

2. **Required Python Libraries to be installed before running**:
   - dash
   - pandas
   - dash-bootstrap-components
   - plotly.express
   - requests


---

## Getting Started

### Running the WebAPI

1. **Clone the Repository**:

2. **Run the Application**:  
Start the WebAPI by running `main.py`.

---

## Development Structure

The project follows this modular structure:

- **`main.py`**: The main entry point for running the WebAPI.
- **`Setting_Layout.py`**: Responsible for setting up layouts and statistics for the `generalDashboard.py` page.
- **`web_api.py`**: Converts data from an external API into a pandas DataFrame for further processing.
- **`API_Grabber_to_database.py`**: Grabs and processes data from the API, creating a local SQLite database named `database.db`.

### Pages Folder:
- **`generalDashboard.py`**: A dashboard page that displays general library statistics.
- **`Visualizations.py`**: A dashboard page that plots time-series graphs of columns extracted from the database.
- **`Natural Language Query.py`**: This is functional but need refinement to improve model output of SQL query
### Other Scripts:
- **`Data exploration.py`**: For local data inspection and exploration. This script is for analysis purposes and is not part of the main WebAPI.

---

## Basic Knowledge for Dash Development

Here are some key concepts for working with Dash:

1. **`app = Dash()`**: The core constructor responsible for initializing the app.
2. **`layout`**: Defines the front-end components displayed in the browser.
3. **`@callback`**: Allows interaction between components (responding to user input).
