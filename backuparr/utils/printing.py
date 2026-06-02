import sys

from backuparr.utils.colors import bcolors


def printException(e):
    print(f"{bcolors.RED}An Error occurred:\n"
          f"{str(e)}{bcolors.ENDC}")

def printExit():
    print(f"{bcolors.RED}User terminated the process...{bcolors.ENDC}")
    sys.exit()

def customExit(message):
    sys.exit(f"{bcolors.RED}{message}{bcolors.ENDC}")

def printError(message):
    print(f"{bcolors.RED}{message}{bcolors.ENDC}")