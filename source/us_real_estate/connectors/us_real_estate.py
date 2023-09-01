import requests
import pandas as pd

class UsRealEstateApiClient:

    def __init__(self, api_key: str, api_host: str):
        self.base_url = "https://us-real-estate.p.rapidapi.com/v2/sold-homes-by-zipcode"
        if api_key is None: 
            raise Exception("API key cannot be set to None.")
        self.api_key = api_key
        if api_host is None: 
            raise Exception("API secret key cannot be set to None.")
        self.api_host = api_host
    
    def get_listings(self, zipcode: str) -> list[dict]:
        """
        Get the real estate listings for a specified zipcode. 

        Args: 
            zipcode: zipcode to search for real estate listings
        
        Returns: 
            A list of trades for a given stock ticket between the start and end times 
        
        Raises:
            Exception if response code is not 200. 
        """
        # API endpoint
        url = self.base_url

        # Variable for zipcode
        querystring = {"zipcode": zipcode, "offset": "0", "limit": "300"}

        headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": self.api_host
        }

        response = requests.get(url, headers=headers, params=querystring)
        if response.status_code == 200 and 'results' in response.json()['data']['home_search'] and response.json()['data']['home_search']['results']:
            filtered = response.json()['data']['home_search']
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
                            ]].copy()
            
            # Replace periods in column names with underscore to fit Postgres column naming conventions
            df_filtered.columns = df_filtered.columns.str.replace("[.]", "_", regex=True)
            # Change list_date and description_sold_date to timestamp data types
            df_filtered['list_date'] = pd.to_datetime(df_filtered['list_date'])
            df_filtered['description_sold_date'] = pd.to_datetime(df_filtered['description_sold_date'])
            # Convert list_price, description_sqft, and description_lot_sqft to numeric values
            df_filtered['location_address_postal_code'] = pd.to_numeric(df_filtered['location_address_postal_code'])
            df_filtered['list_price'] = pd.to_numeric(df_filtered['list_price'])
            df_filtered['description_sqft'] = pd.to_numeric(df_filtered['description_sqft'])
            df_filtered['description_lot_sqft'] = pd.to_numeric(df_filtered['description_lot_sqft'])

        # return rows that do not contain nulls
        return df_filtered.dropna()