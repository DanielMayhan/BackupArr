import json
import os
import sys
import functions
from api_stuff import radarrapi as api

url = api.baseurl + api.movielist + "?" + api.apikey

## Attempt Reconnection
while True:
    (established_connection, radarr_data) = functions.connectToUrl(url, api.baseurl)

    if established_connection:
        print("Connection successful")
        break

    while True:
        choice = input("Connection failed. Try again? [y/n]: ").lower().strip()
        if choice == "n": sys.exit("User terminated the process")
        elif choice == "y":
            print("Reconnecting...")
            break

        else: print("Invalid input. Use: y/n")


filename = "data.json"
filehandle = ""
jsondata = {}

## Check if File Exists
if not os.path.isfile(filename):
    open(filename, "x")
    print("Creating: ", filename)
    filehandle = open(filename, "r")
else :
    print("Found:", filename)
    filehandle = open(filename, "r")


len_data = len(radarr_data)
if len_data == 1:
    print(len_data, "movie have been found.")
elif len_data == 0:
    print("No movie have been found.")
    print("Exiting...")
    sys.exit("No Movies found.")
else:
    print(len_data, "movies have been found.")


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

print("Data has been writen to:", filename)
print("Exiting...")