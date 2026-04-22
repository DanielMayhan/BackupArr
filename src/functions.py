import requests, sys
from requests.exceptions import HTTPError, Timeout, RequestException

def attemptConnection(connectionUrl):
    while True:
        (connected, jsonData) = getJsonDataFromUrl(connectionUrl)

        if connected: return jsonData

        while True:
            choice = input("Connection failed, make sure the URL is valid and accessible. (y)Reconnect | (n) Exit: ").lower().strip()
            if choice == "n": sys.exit("User terminated the process")
            elif choice == "y":
                print("Reconnecting...")
                break
            else: print("Invalid input. Use: y/n")


def getJsonDataFromUrl(connectionUrl):
    noApiUrl = connectionUrl.split("?apiKey=")[0]
    try:
        print("Connecting to " + noApiUrl + "...")
        response = requests.get(connectionUrl, timeout=10).json()
        print("Successfully got Data")
        return True, response
    except Timeout:
        print("Error: The request timed out. This URL might be down or slow.\n@:", noApiUrl)
        return False, ""
    except ConnectionError:
        print("Error: Failed to connect to this URL. Check your URL or network.\n@:", noApiUrl)
        return False, ""
    except HTTPError as e:
        print(f"HTTP Error: {e}\n@:", noApiUrl)
        return False, ""
    except RequestException as e:
        print(f"An ambiguous error occurred: {e}\n@:", noApiUrl)
        return False, ""
    except ValueError:
        print("Error: Successfully connected, but received invalid JSON.\n@:", noApiUrl)
        return False, ""

def makeJsonData(index, data):
    try:
        jsonData =  {
        "title": str(data[index]["title"]),
        "cleanTitle": str(data[index]["cleanTitle"]),
        "imdbId": str(data[index]["imdbId"]),
        "tmdbId": int(data[index]["tmdbId"]),
        "monitored": bool(data[index]["monitored"]),
        "quality": int(data[index]["movieFile"]["quality"]["quality"]["resolution"])
        }
        return jsonData
    except KeyError:
        print("KeyError: Important Data not found!")
        sys.exit()

def getNumUserInput(lastnum):
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