import shutil
from pathlib import Path

from dotenv import dotenv_values, set_key


def run():
    baseDir = Path(__file__).resolve().parent

    envFilepath = baseDir / ".env"
    envExampleFilepath = baseDir / ".env.example"

    print("Setting up Backuparr, copying .env file...")
    shutil.copy(envExampleFilepath, envFilepath)

    envData = dotenv_values(envFilepath)

    print("--------------Env Setup--------------")
    for key in envData.keys():
        value = input(f"Please enter the value for {key}: ").strip()
        set_key(envFilepath, key, value)
        print(f"Set {key} to: {value}")
        print(f"-" * 50)

    print("All .env settings are set, you are good to go!")
    print("To run Backuparr, use command: 'backuparr [backup|restore] [radarr|sonarr] [filename]'")
    print("Exiting.......")


if __name__ == "__main__":
    run()