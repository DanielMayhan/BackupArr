import requests
from requests.exceptions import HTTPError, Timeout, RequestException


def getJsonDataFromUrl(url, baseurl):
        try:
            print("Connecting to " + baseurl + "...")
            response = requests.get(url, timeout=10).json()
            response.raise_for_status()
            return True, response
        except Timeout:
            print("Error: The request timed out. This URL might be down or slow.\n@:", baseurl)
            return False, ""
        except ConnectionError:
            print("Error: Failed to connect to this URL. Check your URL or network.\n@:", baseurl)
            return False, ""
        except HTTPError as e:
            print(f"HTTP Error: {e}\n@:", baseurl)
            return False, ""
        except RequestException as e:
            print(f"An ambiguous error occurred: {e}\n@:", baseurl)
            return False, ""
        except ValueError:
            print("Error: Successfully connected, but received invalid JSON.\n@:", baseurl)
            return False, ""

def getimdbID(moviedata):
    return moviedata["imdbId"]

def gettmdbID(moviedata):
    return moviedata["tmdbId"]

def makeJsonData(index, data):
    return {
        "title": str(data[index]["title"]),
        "cleanTitle": str(data[index]["cleanTitle"]),
        "imdbId": str(data[index]["imdbId"]),
        "tmdbId": int(data[index]["tmdbId"]),
        "monitored": bool(data[index]["monitored"])
    }