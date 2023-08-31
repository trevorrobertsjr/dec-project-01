from dotenv import load_dotenv
import os
import requests
import pandas as pd
import numpy as np


def fetch_data_by_zipcode(zipcode, API_KEY, API_HOST):

    # API endpoint
    url = "https://us-real-estate.p.rapidapi.com/v2/sold-homes-by-zipcode"

    # Variable for zipcode
    querystring = {"zipcode": zipcode, "offset": "0", "limit": "300"}

    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": API_HOST
    }

    response = requests.get(url, headers=headers, params=querystring)
    return response


def process_and_store_data(response, zipcode):
    # Create a dictionary from JSON file with the home search results only
    if response.status_code == 200:

        filtered = response.json()['data']['home_search']

        # Check if ‘results’ exists and is not empty
        if 'results' in filtered and filtered['results']:

            # Flatten nested JSON
            df = pd.json_normalize(filtered, record_path=['results'])

            # Create a new dataframe from only the interesting columns
            df_filtered=df[['permalink',
                            'list_price',
                            'list_date',
                            'description.sold_date',
                            'location.address.postal_code',
                            'location.county.name',
                            'location.address.city',
                            'location.address.state',
                            'description.sqft',
                            'description.lot_sqft'
                            ]]
            
            # Replace periods in column names with underscore to fit Postgres column naming conventions
            df_filtered.columns = df_filtered.columns.str.replace("[.]", "_", regex=True)

            # Write command to write df_filtered to a file (this will be the 300 jsons)
            df_filtered.to_json(r"output-data/json/" + zipcode + ".json")

            filename = "output.csv"

            # Check if the CSV file already exists
            file_exists = os.path.isfile(f"./output-data/csv/{filename}")

            if file_exists:

                # If file exists, append without header
                df_filtered.to_csv(f"./output-data/csv/{filename}", mode='a', header=False, index=False)

            else:

                # If file doesn't exist, create and write with header
                df_filtered.to_csv(f"./output-data/csv/{filename}", mode='w', header=True, index=False)
                file_exists = True

        else:
            print(f"Zipcode: {zipcode} has no results")

    else:
        print(f"Zipcode: {zipcode} failed with status code {response.status_code}")


def main():

    load_dotenv()
    api_key = os.environ.get("X-RapidAPI-Key")
    api_host = os.environ.get("X-RapidAPI-Host")

    # Method 1
    #This turns the column into a string and keeps the leading zeros.
    zip_code_list = pd.read_csv("input-data/zipcodes.csv", dtype={'zipcodes': 'str'}, header=0)['zipcodes'].tolist()

    # Method 2
    # #This turns column into a string
    # zip_code_list = pd.read_csv("input-data/zipcodes.csv", header=0)['zipcodes'].astype(str)
    # # This puts zeros at the beginning of the zipcodes that are missing them.
    # zip_code_list = zip_code_list.str.zfill(5)


    # TODO
    # EDIT THE CODE, SO IT ISN'T LIKE SPAGHETTI CODE AND ADD CLASSES/METHODS LIKE THE LESSONS IN CLASS.

    for zipcode in zip_code_list:
        response = fetch_data_by_zipcode(zipcode, api_key, api_host)
        process_and_store_data(response, zipcode)

    output_wo_nulls = pd.read_csv("output-data/csv/output.csv", header=0).dropna()
    output_wo_nulls.to_csv("output-data/csv/output_wo_nulls.csv", header=True, index=False)


if __name__ == "__main__":
    main()
    
