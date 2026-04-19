import requests
from requests.exceptions import HTTPError, Timeout, RequestException

def connectToRadarr(url):
        try:
            print("Connecting to Radarr...")
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            radarr_data = response.json()
            print("Connection successful, Movie data Acquired")
        except Timeout:
            print("Error: The request timed out. Radarr might be down or slow.")
        except ConnectionError:
            print("Error: Failed to connect to Radarr. Check your URL or network.")
        except HTTPError as e:
            print(f"HTTP Error: {e}")
        except RequestException as e:
            print(f"An ambiguous error occurred: {e}")
        except ValueError:
            print("Error: Successfully connected, but received invalid JSON.")


def getimdbID(moviedata):
    return moviedata["imdbId"]

def gettmdbID(moviedata):
    return moviedata["tmdbId"]

def makejsondata(title, cleanTitle, imdbID, tmdbID, monitored):
    jsondata = {
        "title": str(title),
        "cleanTitle": str(cleanTitle),
        "imdbID": str(imdbID),
        "tmdbID": int(tmdbID),
        "monitored": bool(monitored)
    }
    return jsondata

def getjsondata(index, data):
    return makejsondata(data[index]["title"], data[index]["cleanTitle"], data[index]["imdbId"], data[index]["tmdbId"], data[index]["monitored"])