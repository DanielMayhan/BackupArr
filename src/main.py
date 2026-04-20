import json, os, sys

import requests
from requests import *

import functions
from api_stuff import radarrapi as api

baseurl = api.baseurl + api.movielist
url = baseurl + "?" + api.apikey
radarr_data = {}

## Trying to Establish connection to Radarr
try:
    print("Connecting to Radarr...")
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    radarr_data = response.json()
    print("Connection successful")
except Timeout:
    print("Error: The request timed out. Radarr might be down or slow.\n@:", baseurl, "\nExiting...")
    sys.exit("Error: The request timed out. Radarr might be down or slow.")
except ConnectionError:
    print("Error: Failed to connect to Radarr. Check your URL or network.\n@:", baseurl, "\nExiting...")
    sys.exit("Error: Failed to connect to Radarr. Check your URL or network.")
except HTTPError as e:
    print(f"HTTP Error: {e}\n@:", baseurl, "\n Exiting...")
    sys.exit(e)
except RequestException as e:
    print(f"An ambiguous error occurred: {e}\n@:", baseurl, "\nExiting...")
    sys.exit(e)
except ValueError:
    print("Error: Successfully connected, but received invalid JSON.\n@:", baseurl, "\nExiting...")
    sys.exit("Error: Successfully connected, but received invalid JSON.")


len_data = len(radarr_data)
if len_data == 1:
    print(len_data, "movie have been found.")
else:
    print(len_data, "movies have been found.")


filename = "../data.json"
filehandle = ""
jsondata = {}

## Check if File Exists
if not os.path.isfile(filename):
    open(filename, "x")
    print("Creating: ", filename)
    filehandle = open(filename, "r")
else :
    print("File exists")
    filehandle = open(filename, "r")

## Make sure file is not empty
if os.path.exists(filename) and os.path.getsize(filename) > 0:
    with open(filename, 'r') as f:
        jsondata = json.load(f)
else:
    print(filename, "is empty.")
filehandle.close()

## Making and writing data to json file
for i in range(len_data):
    jsondata[str(radarr_data[i]["tmdbId"])] = functions.getjsondata(i, radarr_data)
    print("Writing data for: ", radarr_data[i]["title"])

with open(filename, "w", encoding="utf-8") as f:
    json.dump(jsondata, f, indent=4, ensure_ascii=False, sort_keys=True)