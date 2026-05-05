import json
import sys

import api_stuff as api
import functions


def run(app, path):
    ## Resolving Filename
    filename = functions.resolveFilename(path)

    ## Required API Calls
    rootFolder = ""
    qualityProfiles = ""
    match app:
        case "radarr":
            rootFolder = functions.attemptConnection(api.radarr.rootFolderUrl, api.radarr.apiKey)
            qualityProfiles = functions.attemptConnection(api.radarr.qualityProfileUrl, api.radarr.apiKey)
        case "sonarr":
            rootFolder = functions.attemptConnection(api.sonarr.rootFolderUrl, api.sonarr.apiKey)
            qualityProfiles = functions.attemptConnection(api.sonarr.qualityProfileUrl, api.sonarr.apiKey)

    
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
    jsonDataList = []
    for movie, details in backupdata.items():
        match app:
            case "radarr":
                id_text = "tmdbId"
                id_cont = details["tmdbId"]
            case "sonarr":
                id_text = "tvdbId"
                id_cont = details["tvdbId"]

        jsonDataList.append({
            "title": str(details["title"]),
            str(id_text): int(id_cont),
            "qualityProfileId": quality_dictionary[int(details["quality"])],
            "rootFolderPath": str(selectedRootFolderPath),
            "monitored": bool(details["monitored"]),
        })

    # match app:
    #     case "radarr":
    #         headers = {"x-api-key" : api.radarr.apiKey}
    #         resp = requests.post(api.radarr.movieListUrl, headers=headers, json=jsonbody)
    #     case "sonarr":
    #         headers = {"x-api-key": api.sonarr.apiKey}
    #         resp = requests.post(api.sonarr.seriesListUrl, headers=headers, json=jsonbody)
    # print("Imported: " + str(details["title"]))
    # print(str(resp.elapsed.total_seconds()) + "s")
    # print(resp.status_code)

    match app:
        case "radarr":
            functions.postJsonData(api.radarr.movieListUrl, api.radarr.apiKey, jsonDataList)
        case "sonarr":
            functions.postJsonData(api.sonarr.seriesListUrl, api.sonarr.apiKey, jsonDataList)

    print("Successfully imported all entries.\nExiting...")
    sys.exit()

if __name__ == "__main__":
    run()