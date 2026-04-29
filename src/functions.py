from pathlib import Path

import requests
import sys
from requests.exceptions import HTTPError, Timeout, RequestException


def attemptConnection(connectionUrl, apiKey):
    while True:
        (connected, jsonData) = getJsonDataFromUrl(connectionUrl, apiKey)
        if connected: return jsonData
        while True:
            choice = input("Connection failed, make sure the URL is valid and accessible. (y)Reconnect | (n) Exit: ").lower().strip()
            if choice == "n": sys.exit("User terminated the process")
            elif choice == "y":
                print("Reconnecting...")
                break
            else: print("Invalid input. Use: y/n")

# TODO: Added 401 Unauthorized Error
def getJsonDataFromUrl(connectionUrl, apiKey):
    noApiUrl = connectionUrl.split("?apiKey=")[0]
    try:
        print("Connecting to " + noApiUrl)
        headers = {"x-api-key" : apiKey}
        response = requests.get(connectionUrl, headers=headers, timeout=10).json()
        print("Connection established.")
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
        if data[index].get("movieFile") is not None: quality = data[index]["movieFile"]["quality"]["quality"]["resolution"]
        else: quality = -1

        jsonData =  {
        "title": str(data[index]["title"]),
        "tmdbId": int(data[index]["tmdbId"]),
        "monitored": bool(data[index]["monitored"]),
        "quality": int(quality)
        }
        return jsonData
    except Exception as e:
        print("KeyError: Important Data not found!")
        print(str(e))
        sys.exit()

def getNumUserInput(lastnum):
    while True:
        num = input("Enter choice, default [0]: ").strip()
        try:
            if not num: return 0
            num = int(num)
            if int(num) <= lastnum: return int(num)
            else: print(str(num) + " is not a integer, or a valid input...")

        except ValueError:
            print(str(num) + " is not a valid input...")

def resolveFilename(path):
    filename = Path(path).resolve()
    try:
        filename.parent.mkdir(parents=True, exist_ok=True)
        return filename
    except Exception as e:
        print("An Error occured: " + str(e))