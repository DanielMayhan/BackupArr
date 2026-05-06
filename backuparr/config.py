import sys
from pathlib import Path

from dotenv import dotenv_values, set_key

from backuparr import functions


def run():
    baseDir = Path(__file__).resolve().parent

    envFilepath = ".env"
    envData = dotenv_values(envFilepath)

    while True:
        print("----------------Configurator-----------------")
        print("Which of the values would you like to change?")

        keyDict = list(envData.keys())

        for i in range(len(keyDict)):
            print(f"[{i}] | {keyDict[i]} | {envData[keyDict[i]]}")

        choice = functions.getNumUserInput(len(keyDict) - 1)

        newValue = input(f"Please enter the new values for {keyDict[choice]}: ").strip()

        set_key(envFilepath, str(keyDict[choice]), newValue)

        print(f"Set {keyDict[choice]} to {newValue}")

        if not functions.getBoolUserInput("Would you like to change another value? (y/n): "):
            sys.exit("Exiting...")


if __name__ == "__main__":
    run()