import os
import requests

from utils import utils

radarr_apikey = str(os.getenv("API_KEY"))
radarr_url = "http://127.0.0.1:7878"
api_url = "/api/v3/movie?apiKey="
url = radarr_url + api_url + radarr_apikey



response = requests.get(url)
data = response.json()
len_data = len(data)

print("---------------------------------------------------------------------------------------------------------")

for i in range(len_data):
    if data[i]["hasFile"]:
        print("Title: " + data[i]["title"])
        print("ID: " + str(data[i]["id"]))
        print("Magnet Link: " + utils.getmagnetlink(data[i]["id"]))
        print("---------------------------------------------------------------------------------------------------------")