import pandas as pd
import json

# Open source JSON file
inputfile = open('extract-data.json')

# Create a dictionary from JSON file with the home search results only
filtered=json.load(inputfile)['data']

# Flatten nested JSON
df = pd.json_normalize(filtered, record_path=['results'])

# Create a new dataframe from only the interesting columns
df_filtered = df[['permalink','list_price','list_date','description.year_built','location.address.postal_code','location.county.name','location.address.city','location.address.state', "description.sold_date"]]
print(df_filtered)

# can test for loop here with small sample size (2 zipcodes)