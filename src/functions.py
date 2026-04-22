import requests
from requests.exceptions import HTTPError, Timeout, RequestException

from api_stuff import radarrapi as api

def connectToRadarr(url):
        try:
            print("Connecting to Radarr...")
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            response_data = response.json()
            return True, response_data
        except Timeout:
            print("Error: The request timed out. Radarr might be down or slow.\n@:", api.baseurl)
            return False, ""
        except ConnectionError:
            print("Error: Failed to connect to Radarr. Check your URL or network.\n@:", api.baseurl)
            return False, ""
        except HTTPError as e:
            print(f"HTTP Error: {e}\n@:", api.baseurl)
            return False, ""
        except RequestException as e:
            print(f"An ambiguous error occurred: {e}\n@:", api.baseurl)
            return False, ""
        except ValueError:
            print("Error: Successfully connected, but received invalid JSON.\n@:", api.baseurl)
            return False, ""

def getimdbID(moviedata):
    return moviedata["imdbId"]

def gettmdbID(moviedata):
    return moviedata["tmdbId"]

def makejsondata(title, cleanTitle, imdbID, tmdbID, monitored, quality):
    jsondata = {
        "title": str(title),
        "cleanTitle": str(cleanTitle),
        "imdbID": str(imdbID),
        "tmdbID": int(tmdbID),
        "monitored": bool(monitored),
        "quality": int(quality)
    }
    return jsondata

def getjsondata(index, data):
    return makejsondata(data[index]["title"], data[index]["cleanTitle"], data[index]["imdbId"], data[index]["tmdbId"], data[index]["monitored"], data[index]["movieFile"]["quality"]["quality"]["resolution"])

def getnumuserinput(lastnum):
    while True:
        num = input("Enter choice, default [0]: ").strip()

        try:
            if not num:
                return 0

            num = int(num)

            if int(num) <= lastnum:
                return int(num)

            else:
                print(str(num) + " is not a integer, or a valid input...")
        except ValueError:
            print(str(num) + " is not a valid input...")