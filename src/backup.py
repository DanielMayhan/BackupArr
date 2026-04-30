import enum
import json
import sys

import requests

import functions
import api_stuff as api

def run(app, filename):
    ## Resolving Filename
    filename = functions.resolveFilename(filename)

    ## Attempt Connection
    movieData = {}
    match app:
        case "radarr":
            movieData = functions.attemptConnection(api.radarr.movieListUrl, api.radarr.apiKey)
        case "sonarr":
            movieData = functions.attemptConnection(api.sonarr.seriesListUrl, api.sonarr.apiKey)

    ## Display found movies
    len_data = len(movieData)
    if len_data == 1:
        print(len_data, "movie/series have been found.")
    elif len_data == 0:
        print("No movie/series have been found.")
        print("Exiting...")
        sys.exit("No movies/series found.")
    else:
        print(len_data, "movies/series have been found.")

    #TODO: Sonarr Backup | Title, tvdbId, qualityProfileId, rootFolder, monitored
    ## Making and writing data to JSON file
    jsondata = {}
    for i in range(len_data):
        print("Writing Data for: " + str(movieData[i]["title"]))

        match app:
            case "radarr":
                jsondata[str(movieData[i]["tmdbId"])] = functions.makeJsonData(i, movieData)
            case "sonarr":
                quality = -1
                print("1")
                if int(movieData[i]["statistics"]["episodeFileCount"]) > 0:
                    req = requests.get(api.sonarr.episodeFileUrl + "?seriesId=" + str(movieData[i]["id"]), headers={"x-api-key": api.sonarr.apiKey}).json()
                    for j in range(len(req)):
                        try:
                            quality = int(req[j]["quality"]["quality"]["resolution"])
                            break
                        except Exception as e:
                            print("Resolution not found, trying another file...")
                print(2)
                jsondata[str(movieData[i]["tvdbId"])] = functions.makeSonarrData(i, movieData, quality)

        print("Writing Data for: " + str(movieData[i]["title"]))

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(jsondata, f, indent=4, ensure_ascii=False, sort_keys=True)

    print("Data has been writen to:", filename)
    print("Exiting...")

if __name__ == "__main__":
    run()