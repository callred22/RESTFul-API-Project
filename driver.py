import pandas as pd 
import requests 

def fetch_data_from_api(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status() # Raise an exception for 4xx or 5xx status codes
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return None

api_url_1 = "https://data.cms.gov/data-api/v1/dataset/d7fabe1e-d19b-4333-9eff-e80e0643f2fd/data"

data_1 = fetch_data_from_api(api_url_1)

if data_1:
    print(data_1) # or do whatever you want with the data
else:
    print("Failed to fetch data from API.")

medenroll_df = pd.json_normalize(data_1)
medenroll_df



api_url_3 = "https://data.cms.gov/data-api/v1/dataset/2684c3e2-3598-4997-a598-0991bad6fbf2/data"

data_3 = fetch_data_from_api(api_url_3)

if data_3:
    print(data_3) # or do whatever you want with the data
else:
    print("Failed to fetch data from API.")

covidhosp_df = pd.json_normalize(data_3)
covidhosp_df



api_url_2 = "https://raw.githubusercontent.com/millbj92/US-Zip-Codes-JSON/master/USCities.json"

data_2 = fetch_data_from_api(api_url_2)

if data_2:
    print(data_2) # or do whatever you want with the data
else:
    print("Failed to fetch data from API.")

statezip_df = pd.json_normalize(data_2)
statezip_df