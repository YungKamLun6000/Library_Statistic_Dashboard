import pandas as pd
import sqlite3

cnx = sqlite3.connect(r'C:\Users\kamlyung2\PycharmProjects\WelcomeScreen\Library_statistics\database.db')
df = pd.read_sql_query('''SELECT * FROM Library_stats''', cnx)
df = df.drop(df[df["Year"] == 2016].index)
df = df.reset_index()
df["date"] = pd.to_datetime(df["Year"].astype(str) + "-" + df["Month"].astype(str))

group = df.groupby("DisplayName")

duplicate_names = df["DisplayName"].value_counts()
duplicate_names = duplicate_names[duplicate_names > 1].index
result_list = duplicate_names.tolist()

#print(df.isnull().sum())

month_interval = []
year_interval = []
broken_interval = []

for name in result_list:
    test = group.get_group(name)

    start_date = test["date"].min().to_period('M').to_timestamp()
    end_date = test["date"].max().to_period('M').to_timestamp()
    test_dates = pd.to_datetime(test["date"]).dt.to_period('M').dt.to_timestamp()

    full_month_range = pd.date_range(start=start_date, end=end_date, freq='MS')
    missing_months = full_month_range.difference(test_dates)

    if len(missing_months) == 0:
        month_interval.append(name)
    else:
        yearly_start = pd.to_datetime("2017-06-01")
        yearly_end = pd.to_datetime(f"{end_date.year}-06-01")

        if start_date < yearly_start and end_date < yearly_start:
            broken_interval.append(name)
            continue

        full_year_range = pd.date_range(start=yearly_start, end=yearly_end, freq=pd.DateOffset(years=1))

        expected_years = full_year_range.year
        actual_years = test["date"].dt.year.unique()

        missing_years = [y for y in expected_years if y not in actual_years]

        if len(missing_years) == 0:
            year_interval.append(name)
        else:
            broken_interval.append(name)
print(year_interval)
print(month_interval)