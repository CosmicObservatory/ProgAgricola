from config.datasources import URL_API_NASAPOWER
from config.paths import PATH_ROOT
from yarl import URL
import requests
import pandas as pd

model_parameters = pd.read_csv(PATH_ROOT / "config" / "nasa-power-parameters.csv")

start = "20030101"
end = "20040101"
laritude, longitude = -10, 10
community = "ag"
parameters = model_parameters['ID'].to_list()
header = "true"
units = "metric"
format = "json"

api_parameters = {
    "start": start,
    "end": end,
    "latitude": laritude,
    "longitude": longitude,
    "community": community,
    "parameters": parameters,
    "format": format
    }

call = URL(URL_API_NASAPOWER).with_query(api_parameters)
response = requests.get(call)
print(response.json().keys())