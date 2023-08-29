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
    # zipcode_list_2 = ["35649", "35749"]
    zipcode_list_2 = ["10003"]

    #for loop
    for zipcode in zipcode_list_2:
        
        # API endpoint
        url = "https://us-real-estate.p.rapidapi.com/v2/sold-homes-by-zipcode"

    # need to create for loop. Need to use variable for zipcode.
        querystring = {"zipcode":zipcode,"offset":"0","limit":"42"}

        headers = {
            "X-RapidAPI-Key": os.environ.get("X-RapidAPI-Key"),
            "X-RapidAPI-Host": os.environ.get("X-RapidAPI-Host")
        }
        # Make API call to retrieve for sale properties by zip code
        response = requests.get(url, headers=headers, params=querystring)
        # print(response.json())

        # Create a dictionary from JSON file with the home search results only
        filtered = response.json()['data']['home_search']
        # print(filtered)

        # # Flatten nested JSON
        df = pd.json_normalize(filtered, record_path=['results'])
        # print(df)

        # # Create a new dataframe from only the interesting columns
        df_filtered = df[['permalink','list_price','list_date','description.sold_date', 'location.address.postal_code','location.county.name','location.address.city','location.address.state', 'description.sqft', 'description.lot_sqft']]
        df_filtered.to_json(r"output-data/"+zipcode+".json")

    # need to write command to write df_filtered to a file (this will be the 300 jsons)

    