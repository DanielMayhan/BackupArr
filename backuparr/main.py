import sys

from backuparr import backup, restore


def run():
    if len(sys.argv) != 4:
        print("Usage: backuparr [backup|restore] [radarr|sonarr] [filename]")
        return

    mode = str(sys.argv[1].lower().strip())
    app = str(sys.argv[2].lower().strip())
    filename = str(sys.argv[3])

    if (app != "radarr") and (app != "sonarr"):
        print(app)
        sys.exit("Argument Error, 2. Argument must be 'radarr' or 'sonarr'")

    if mode == "backup":
        backup.run(app, filename)
    elif mode == "restore":
        restore.run(app, filename)
    else:
        print("Argument Error, Usage: backuparr [backup|restore] [radarr|sonarr] [filename]")

if __name__ == "__main__":
    run()