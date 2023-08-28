# https://rapidapi.com/datascraper/api/us-real-estate
# v2 for sale by zip

# work-in-progress

from dotenv import load_dotenv
import os
import requests
import pandas as pd

if __name__ == "__main__":
    # Load environment data from .env
    load_dotenv()

    # API endpoint
    url = "https://us-real-estate.p.rapidapi.com/v2/sold-homes-by-zipcode"

# need to create for loop. Need to use variable for zipcode.
    querystring = {"zipcode":"10005","offset":"0","limit":"42"}

    headers = {
        "X-RapidAPI-Key": os.environ.get("X-RapidAPI-Key"),
        "X-RapidAPI-Host": os.environ.get("X-RapidAPI-Host")
    }
    # Make API call to retrieve for sale properties by zip code
    response = requests.get(url, headers=headers, params=querystring)

    # Create a dictionary from JSON file with the home search results only
    filtered = response.json()['data']['home_search']

    # Flatten nested JSON
    df = pd.json_normalize(filtered, record_path=['results'])

    # Create a new dataframe from only the interesting columns
    df_filtered = df[['permalink','list_price','list_date','description.year_built','location.address.postal_code','location.county.name','location.address.city','location.address.state']]
    print(df_filtered)

    # need to write command to write df_filtered to a file (this will be the 300 jsons)
    