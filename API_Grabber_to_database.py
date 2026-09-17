import web_api


url = f"https://app.lib.cityu.edu.hk/power_bi_api/api/statistics/range?startYear=2015&startMonth=1&endYear=2026&endMonth=12"
data = web_api.Dataapi_import(url)

web_api.pd_to_sqlite3(data)
