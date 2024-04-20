import pandas as pd 
import requests 

def fetch_data_from_api(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status() # Raise an exception for 4xx or 5xx status codes
        data = response.json()
        # return pd.json_normalize(data)
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return None