import json
import sys
import requests

from pathlib import Path
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

def getJsonDataFromUrl(connectionUrl, apiKey):
    noApiUrl = connectionUrl.split("?apiKey=")[0]
    try:
        print("Connecting to " + noApiUrl)
        headers = {"x-api-key" : apiKey}
        response = requests.get(connectionUrl, headers=headers, timeout=10)
        if response.status_code == 401:
            print("Error: 401 Request unauthorized. @:", noApiUrl)
            return False, ""
        print("Connection established.")
        return True, response.json()
    except Timeout:
        print("Error: The request timed out. This URL might be down or slow. @:", noApiUrl)
        return False, ""
    except ConnectionError:
        print("Error: Failed to connect to this URL. Check your URL or network. @:", noApiUrl)
        return False, ""
    except HTTPError as e:
        print(f"HTTP Error: {e}\n@:", noApiUrl)
        return False, ""
    except RequestException as e:
        print(f"An ambiguous error occurred: {e}\n@:", noApiUrl)
        return False, ""
    except ValueError:
        print("Error: Successfully connected, but received invalid JSON. @:", noApiUrl)
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

def makeSonarrData(index, data, quality):
    try:
        jsonData = {
        "title": str(data[index]["title"]),
        "tvdbId": int(data[index]["tvdbId"]),
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
        print("An Error occurred: " + str(e))

def postJsonData(connectionUrl, apiKey, jsonDataList):
    statusDict = {}
    print("Attempting to post data for " + str(len(jsonDataList)) + " entries...")
    for index, item in enumerate(jsonDataList):
        try:
            print("Importing: " + item["title"])
            req_response = requests.post(connectionUrl, headers={"x-api-key" : apiKey}, json=item)
            if not req_response.status_code == 201:
                statusDict[index] = req_response
            print("Code: " + str(req_response.status_code) + " | " + str(req_response.elapsed.total_seconds()) + "s")
        except Exception as e:
            print("An Error occurred: " + str(e))

    while True:
        if len(statusDict) == 0: return

        print("Successfully posted data for " + str(len(jsonDataList) - len(statusDict)) + " entries...")

        choice = input("Do you want to retry all entries that didn't return 201 Created? Retry(r) | List(l) | Default: Exit(e): ").strip().lower()
        if not choice or choice == "e":
            sys.exit("User terminated process.")
        elif choice == "l":
            for j, resp in statusDict.items():
                print(f"----- {jsonDataList[j]["title"]} -----")
                print(f"Code: {resp.status_code}")
                print(f"Response:\n{json.dumps(resp.json(), indent=4)}")
                print("-" * 100)

            while True:
                choice2 = input("Do you want to retry importing? (y/n): ").strip().lower()
                if choice2 == "y": break
                elif choice2 == "n": sys.exit("User terminated process.")
                else: print("Invalid Choice, retrying...")
        elif choice == "r": print("Retrying...")
        else:
            print("Invalid Choice, retrying...")
            continue

        toDelete = []
        for k, resp in statusDict.items():
            print("Importing: " + jsonDataList[k]["title"])
            retry_resp = requests.post(connectionUrl, headers={"x-api-key" : apiKey}, json=jsonDataList[k])
            print("Code: " + str(retry_resp.status_code) + " | " + str(retry_resp.elapsed.total_seconds()) + "s")
            if retry_resp.status_code == 201:
                print(f"Successfully posted data for: {jsonDataList[k]["title"]}")
                toDelete.append(k)
            else:
                print(f"Still unable to import: {jsonDataList[k]["title"]}")

        for l in toDelete:
            del statusDict[l]