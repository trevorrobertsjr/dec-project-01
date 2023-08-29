import pandas as pd
import json

# Open source JSON file
inputfile = open('extract-data.json')

# Create a dictionary from JSON file with the home search results only
filtered=json.load(inputfile)['data']

# Flatten nested JSON
df = pd.json_normalize(filtered, record_path=['results'])

# Create a new dataframe from only the interesting columns
df_filtered = df[['permalink','list_price','list_date', 'description.sold_date', 'location.address.postal_code','location.address.city','location.address.state', 'description.sqft', 'description.lot_sqft']]
print(df_filtered)

# Add a write to json folder/file here

# can test for loop here with small sample size (2 zipcodes)
    # lines 4-15


# state_names = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Iowa", "Idaho", "Illinois", "Indiana", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]

# city_names = ["Huntsville", "Anchorage", "Phoenix", "Little Rock", "Los Angeles", "Denver", "Bridgeport", "Wilmington", "Jacksonville", "Atlanta", "Honolulu", "Boise", "Chicago", "Indianapolis", "Des Moines", "Wichita", "Louisville", "New Orleans", "Portland", "Baltimore", "Boston", "Detroit", "Minneapolis", "Jackson", "Kansas City", "Billings", "Omaha", "Las Vegas", "Manchester", "Newark", "Albuquerque", "New York City", "Charlotte", "Fargo", "Columbus", "Oklahoma City", "Portland", "Philadelphia", "Providence", "Charleston", "Sioux Falls", "Nashville", "Houston", "Salt Lake City", "Burlington", "Virginia Beach", "Seattle", "Charleston", "Milwaukee", "Cheyenne"]
