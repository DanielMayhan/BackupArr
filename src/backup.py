import json
import sys

import functions
from api_stuff import radarrapi as api


def run(app, filename):
    ## Resolving Filename
    filename = functions.resolveFilename(filename)

    ## Attempt Connection
    movieData = functions.attemptConnection(api.movieListUrl, api.apikey)

    ## Display found movies
    len_data = len(movieData)
    if len_data == 1:
        print(len_data, "movie have been found.")
    elif len_data == 0:
        print("No movie have been found.")
        print("Exiting...")
        sys.exit("No Movies found.")
    else:
        print(len_data, "movies have been found.")


    ## Making and writing data to json file
    jsondata = {}
    for i in range(len_data):
        jsondata[str(movieData[i]["tmdbId"])] = functions.makeJsonData(i, movieData)
        print("Writing data for: ", movieData[i]["title"])

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(jsondata, f, indent=4, ensure_ascii=False, sort_keys=True)

    print("Data has been writen to:", filename)
    print("Exiting...")

if __name__ == "__main__":
    run()