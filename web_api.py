import pandas as pd
import requests

def Dataapi_import(data1_url):
    Library_data1_url = data1_url

    response1 = requests.get(Library_data1_url)

    data1_json = response1.json()

    df1 = pd.json_normalize(data1_json)
    return df1


def Dataapi_import_nested(data1_url):
    # Step 1: Fetch the API JSON data
    response1 = requests.get(data1_url)
    data1_json = response1.json()

    # Step 2: Extract and normalize the nested "Fields" data
    result = []
    for category in data1_json:
        category_id = category.get("CategoryId", None)
        category_name = category.get("CategoryName", None)

        # Loop through each "Fields" entry in the category
        if "Fields" in category:
            for field in category["Fields"]:
                # Add the category ID and name to each field
                field_data = {
                    "CategoryId": category_id,
                    "CategoryName": category_name,
                    "DisplayName": field.get("DisplayName", None),
                    "DisplayOrder": field.get("DisplayOrder", None),
                    "SourcePath": field.get("SourcePath", None),
                    "ComponentSourcePaths": field.get("ComponentSourcePaths", None),
                }
                result.append(field_data)

    # Step 3: Create a pandas DataFrame from the flattened list
    df = pd.DataFrame(result)

    # Step 4: Expand "ComponentSourcePaths" into separate rows (if needed)
    if not df["ComponentSourcePaths"].isnull().all():
        # Explode the list into multiple rows if it exists
        df = df.explode("ComponentSourcePaths").reset_index(drop=True)

    return df

