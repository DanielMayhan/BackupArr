

def run():
    print("-" * 20)
    print("BackupArr Help")
    print("-" * 10)
    print("Main Backup & Restore command.")
    print("-> backuparr [backup|restore] [radarr|sonarr] [filename].json <-")
    print("-" * 5)
    print("Configures the values of the .env file.")
    print("-> backuparr-config <-")
    print("-" * 5)
    print("Copies the .env file to the correct location and asks for the values. (Only use once at the beginning)")
    print("-> backuparr-init <-")
    print("-" * 5)
    print("Shows this prompt.")
    print("-> backuparr-help <-")
    print("-" * 20)

if __name__ == "__main__":
    run()