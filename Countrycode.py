import click
import requests
import json

API_URL = "https://www.travel-advisory.info/api"
DATA_FILE = "data.json"

# Function to fetch data from the API and save it to a local file
def fetch_and_save_data():
    response = requests.get(API_URL)
    if response.status_code == 200:
        data = response.json()
        with open(DATA_FILE, 'w') as file:
            json.dump(data, file)
        return data
    else:
        print("Failed to fetch data from the API.")
        return None

# Function to load data from a local file
def load_data_from_file():
    try:
        with open(DATA_FILE, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print("Data file not found. Fetching data from the API...")
        return fetch_and_save_data()

# Function to lookup country names by country code
def lookup_country_name(country_code):
    data = load_data_from_file()
    if data and 'data' in data:
        countries = data['data']
        if country_code in countries:
            return countries[country_code]['name']
    return None

@click.command()
@click.option("--countryCode", required=True, multiple=True, help="Country code(s) to lookup")
def lookup(countryCode):
    for code in countryCode:
        country_name = lookup_country_name(code)
        if country_name:
            print(f"{code}: {country_name}")
        else:
            print(f"Country code {code} not found or an error occurred.")

if __name__ == "__main__":
    lookup()
