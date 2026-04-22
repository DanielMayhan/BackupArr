import json
import os
import sys
import functions
from api_stuff import radarrapi as api

url = api.baseurl + api.movielist + "?" + api.apikey

## Attempt Reconnection
returnedData = functions.attemptConnection(api.baseurl + api.movielist + "?" + api.apikey, api.baseurl + api.movielist)

filename = "data.json"
jsondata = {}

## Check if File Exists
if not os.path.isfile(filename):
    open(filename, "x")
    print("Creating: ", filename)
else :
    print(filename, "has been found.")


len_data = len(returnedData)
if len_data == 1:
    print(len_data, "movie have been found.")
elif len_data == 0:
    print("No movie have been found.")
    print("Exiting...")
    sys.exit("No Movies found.")
else:
    print(len_data, "movies have been found.")


## Making and writing data to json file
for i in range(len_data):
    jsondata[str(returnedData[i]["tmdbId"])] = functions.makeJsonData(i, returnedData)
    print("Writing data for: ", returnedData[i]["title"])

with open(filename, "w", encoding="utf-8") as f:
    json.dump(jsondata, f, indent=4, ensure_ascii=False, sort_keys=True)

print("Data has been writen to:", filename)
print("Exiting...")