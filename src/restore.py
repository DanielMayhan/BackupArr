import functions
import json
import requests
import sys

from api_stuff import radarrapi as api


def run(app, path):
    ## Resolving Filename
    filename = functions.resolveFilename(path)

    ## Required API Calls
    rootFolder = functions.attemptConnection(api.rootFolderUrl, api.apikey)
    qualityProfiles = functions.attemptConnection(api.qualityProfileUrl, api.apikey)

    
    ## Selecting Root Folder
    if len(rootFolder) == 0:
        sys.exit("No root folder found, please add a root folder.")

    elif len(rootFolder) == 1:
        selectedRootFolderPath = rootFolder[0]["path"]
        print("Only one root folder found, no selection needed.")

    else:
        print("Choose Root Folder to restore into, default [0]:")

        for i in range(len(rootFolder)):
            print("[" + str(i) + "] | Radarr-ID: " + str(rootFolder[i]["id"]) + " | Accessible: " + str(rootFolder[i]["accessible"]) + " | Free Space: " + str(rootFolder[i]["freeSpace"]) + " | Path: " + str(rootFolder[i]["path"]))

        selectedRootFolderPath = rootFolder[functions.getNumUserInput(len(rootFolder) - 1)]["path"]


    ## Load file
    try:
        with open(filename, 'r') as f:
            backupdata = json.load(f)
            print("Loaded contents of:", filename)
    except Exception as e:
        sys.exit("An Error occurred: " + str(e))


    ## Select Qualities
    qualities_set = set()
    quality_dictionary = {}

    for tmdbID, details in backupdata.items():
        qualities_set.add(details["quality"])

    for x in qualities_set:
        if x == -1:
            print("There where was no Quality Data found for these movies, which Profile should be used for these?")

            for i in range(len(qualityProfiles)):
                print("[" + str(i) + "] | ID: " + str(qualityProfiles[i]["id"]) + " | Name: " + str(qualityProfiles[i]["name"]))

            quality_dictionary[x] = qualityProfiles[functions.getNumUserInput(len(qualityProfiles) - 1)]["id"]

            print("Profile-Id: " + str(quality_dictionary[x]) + " is now associated with the movies that had no data found.")
            break


        print("Which Quality Profile should be used for importing ==> " + str(x) + "P <== movies?")

        for i in range(len(qualityProfiles)):
            print("[" + str(i) + "] | ID: " + str(qualityProfiles[i]["id"]) + " | Name: " + str(qualityProfiles[i]["name"]))

        quality_dictionary[x] = qualityProfiles[functions.getNumUserInput(len(qualityProfiles) - 1)]["id"]

        print(str(x) + "p associated with Profile-Id: " + str(quality_dictionary[x]))


    ## Making data for import
    # TODO: Check Status codes and make Report
    for movie, details in backupdata.items():
        jsonbody = {
            "title": str(details["title"]),
            "tmdbId": int(details["tmdbId"]),
            "qualityProfileId": quality_dictionary[int(details["quality"])],
            "rootFolderPath": str(selectedRootFolderPath),
            "monitored": bool(details["monitored"]),
        }

        headers = {"x-api-key" : api.apikey}
        resp = requests.post(api.movieListUrl, headers=headers, json=jsonbody)

        print("Imported: " + str(details["title"]))
        print(str(resp.elapsed.total_seconds()) + "s")
        print(resp.status_code)

if __name__ == "__main__":
    run()