# BackupArr

> [!NOTE]
> **AI-Generated Documentation:** This README was drafted with the assistance of AI, but none of the Code in this Project was written by AI.

Welcome to the **BackupArr** repository. This project is currently in its early development stages (**Pre-Alpha**) and aims to provide a lightweight, efficient way to "back up" your media library without duplicating large video files.

---

## The Concept
Traditional backups for media libraries are often prohibitively expensive due to massive file sizes. **BackupArr** changes the paradigm: instead of backing up the media files themselves, this tool maps your library metadata back to its source. In the event of data loss, you can restore the library state to your download client to re-acquire the media from the swarm.

---

## Project Status: Alpha
**Warning:** This software is experimental and **Work in Progress**. It is not recommended for production use. Any and all code are subject to radical changes as development progresses.

---

## Installation
1. Get the newest **.whl** file  release from [Releases](https://github.com/DanielMayhan/BackupArr/releases)


2. **Installing the .whl file via pip**
    ```
   pip install /directory/of/file/backuparr-[version].whl
   ```

## Usage
* **Command Structure:**
    ```bash
    backuparr [backup|restore] [radarr|sonarr] [filename].json
* **Example Command:**
    ```bash
    backuparr backup radarr radarr_backup.json
    ```

---

## Roadmap
These are features and code changes that are either currently being worked on or are planned to be implemented later!
* Code Cleanup
* Unification of all text in-/outputs


---

## Getting Started (Development)

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/DanielMayhan/BackupArr.git
    cd BackupArr
    ```

2.  **Configure Environment:**
    Copy the sample configuration and add your Radarr API key & Url.
    ```bash
    cp .env.example .env
    ```
    
---

## Contributing
We welcome all input during these early stages!
* Open an **Issue** to discuss new ideas or report bugs.
* Submit a **Pull Request** to help with early-stage logic.
* Check the **Discussions** tab to help define the project roadmap.

---

## License
This project is licensed under the [MIT License](LICENSE).