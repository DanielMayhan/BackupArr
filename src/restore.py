import requests, sys, functions, os, json
from api_stuff import radarrapi as api


filename = "data.json"


rootfolderurl = api.baseurl + api.rootfolder + "?" + api.apikey
rootFolder = requests.get(rootfolderurl).json()


if len(rootFolder) == 0:
    sys.exit("No root folder found, please add a root folder to Radarr")

elif len(rootFolder) == 1:
    selectedRootFolderPath = rootFolder[0]["path"]
    print("Only one root folder found, no selection needed.")

else:
    print("Choose Root Folder to restore into, default [0]:")

    for i in range(len(rootFolder)):
        print("[" + str(i) + "] | Radarr-ID: " + str(rootFolder[i]["id"]) + " | Accessible: " + str(rootFolder[i]["accessible"]) + " | Free Space: " + str(rootFolder[i]["freeSpace"]) + " | Path: " + str(rootFolder[i]["path"]))

    selectedRootFolderPath = rootFolder[functions.getnumuserinput(len(rootFolder) - 1)]["path"]


## Load file
if os.path.exists(filename) and os.path.getsize(filename) > 0:
    with open(filename, 'r') as f:
        backupdata = json.load(f)
        print("Loaded", filename)
else:
    print(filename, "does not exist, or is empty.")
    sys.exit("Empty Backup File")


## Load Qualities
qualities_set = set()
for tmdbID, details in backupdata.items():
    qualities_set.add(details["quality"])


quality_dictionary = {}
qualityprofiles = requests.get(api.baseurl + api.qprofiles + "?" + api.apikey).json()
for x in qualities_set:
    print("Which Quality Profile should be used for importing ==> " + str(x) + "P <== movies?")

    for i in range(len(qualityprofiles)):
        print("[" + str(i) + "] | ID: " + str(qualityprofiles[i]["id"]) + " | Name: " + str(qualityprofiles[i]["name"]))

    quality_dictionary[x] = qualityprofiles[functions.getnumuserinput(len(qualityprofiles) - 1)]["id"]

    print(str(x) + "p associated with Profile-Id: " + str(quality_dictionary[x]))


while True:
    shouldmonitor = input("Should the imported movies be monitored? [y/n] ").strip().lower()

    if shouldmonitor == "y":
        monitored = True
        break
    elif shouldmonitor == "n":
        monitored = False
        break
    else:
        print("Invalid Input")

reimporturl = api.baseurl + api.movielist + "?" + api.apikey

for movie, details in backupdata.items():
    jsonbody = {
        "title": str(details["title"]),
        "tmdbId": int(details["tmdbID"]),
        "qualityProfileId": quality_dictionary[int(details["quality"])],
        "rootFolderPath": str(selectedRootFolderPath),
        "monitored": bool(monitored),
    }

    resp = requests.post(reimporturl, json=jsonbody)
    print(str(resp.elapsed.total_seconds()) + "s")
    print(resp.status_code)
    print("Imported: " + str(details["title"]))

