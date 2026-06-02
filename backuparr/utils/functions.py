import json
import sys
from pathlib import Path

import requests
from requests.exceptions import Timeout

import backuparr.utils.errors as error
from backuparr.utils.colors import bcolors


def attemptConnection(connectionUrl, apiKey):
    while True:

        (connected, jsonData) = getJsonDataFromUrl(connectionUrl, apiKey)

        if connected:
            return jsonData

        while True:
            choice = input(f"{bcolors.YELLOW}Connection failed, make sure the URL is valid and accessible.{bcolors.ENDC}\n"
                           f"{bcolors.GREEN}(y) Reconnect {bcolors.ENDC}|{bcolors.RED} (n) Exit {bcolors.ENDC}: ").lower().strip()

            if choice == "n":
                error.printExit()

            elif choice == "y":
                print("Reconnecting...")
                break

            else:
                print(f"{bcolors.RED}Invalid input. Use: y/n{bcolors.ENDC}")


def getJsonDataFromUrl(connectionUrl, apiKey):
    noApiUrl = connectionUrl.split("?apiKey=")[0]
    try:

        print(f"Retrieving Data from: {noApiUrl}")
        headers = {"x-api-key" : apiKey}
        response = requests.get(connectionUrl, headers=headers, timeout=10)

        if response.status_code == 401:

            print(f"{bcolors.RED}An Error occurred: 401 Request unauthorized, please check the API-KEY value.{bcolors.ENDC}\n"
                  f"@: {noApiUrl}")
            return False, ""

        return True, response.json()

    except Timeout:
        print(f"{bcolors.RED}An Error occurred: The request timed out. This URL might be down or slow.{bcolors.ENDC}"
              f"\n@: {noApiUrl}")
        return False, ""

    except ConnectionError:
        print(f"{bcolors.RED}An Error occurred: Failed to connect to this URL. Check your URL or network.{bcolors.ENDC}"
              f"\n@: {noApiUrl}")
        return False, ""

    except ValueError:
        print(f"{bcolors.RED}An Error occurred: Successfully connected, but received invalid JSON.{bcolors.ENDC}"
              f"\n@: {noApiUrl}")
        return False, ""

    except Exception as e:
        error.printException(e)
        return False, ""


def makeJsonData(index, data):
    try:
        if data[index].get("movieFile") is not None:
            quality = data[index]["movieFile"]["quality"]["quality"]["resolution"]

        else:
            quality = -1

        jsonData =  {
        "title": str(data[index]["title"]),
        "tmdbId": int(data[index]["tmdbId"]),
        "monitored": bool(data[index]["monitored"]),
        "quality": int(quality)
        }
        return jsonData

    except Exception as e:
        error.printException(e)
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
        error.printException(e)
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
                print(f"{bcolors.RED}{str(num)} is not a integer, or a valid input...{bcolors.ENDC}")

        except ValueError:
            print(f"{bcolors.RED}{str(num)} is not a valid input...{bcolors.ENDC}")


def resolveFilename(path):
    filename = Path(path).resolve()

    try:
        filename.parent.mkdir(parents=True, exist_ok=True)
        return filename

    except Exception as e:
        error.printException(e)


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
            error.printException(e)

    while True:
        if len(statusDict) == 0: return

        print("Successfully posted data for " + str(len(jsonDataList) - len(statusDict)) + " entries...")

        choice = input(f"Do you want to retry all entries that didn't return 201 Created? "
                       f"{bcolors.GREEN}Retry(r) {bcolors.ENDC}| {bcolors.YELLOW}List(l) {bcolors.ENDC}| {bcolors.RED}Default: Exit(e):{bcolors.ENDC} ").strip().lower()

        if not choice or choice == "e":
            error.printExit()

        elif choice == "l":

            for j, resp in statusDict.items():
                print(f"----- {jsonDataList[j]["title"]} -----")
                print(f"Code: {resp.status_code}")
                print(f"Response:\n{json.dumps(resp.json(), indent=4)}")
                print("-" * 100)

            while True:
                choice2 = input(f"Do you want to retry importing? ({bcolors.GREEN}y{bcolors.ENDC}/{bcolors.RED}n{bcolors.ENDC}): ").strip().lower()

                if choice2 == "y":
                    break

                elif choice2 == "n":
                    error.printExit()

                else:
                    print("Invalid Choice, retrying...")

        elif choice == "r":
            print("Retrying...")

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


def getBoolUserInput(message):
    while True:
        choice = input(message).strip().lower()

        if choice == "y":
            return True

        elif choice == "n":
            return False

        else:
            print("Invalid Choice, retrying...")