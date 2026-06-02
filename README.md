# BackupArr

> **AI Notice:** NONE of the Code in this Repository has been written by AI, that being said I did use AI to partially draft this [README.md](https://github.com/DanielMayhan/BackupArr/blob/master/README.md). (I really suck at this stuff...)
---

Welcome to the **BackupArr** repository. This project is currently in its early development stages (**Alpha**) and aims to provide a lightweight, efficient way to "back up" your media library without duplicating large video files.

---

## The Concept
Traditional backups for media libraries are often prohibitively expensive due to massive file sizes. **BackupArr** changes the paradigm: instead of backing up the media files themselves, this tool maps your library metadata back to its source. In the event of data loss, you can restore the library state to your download client to re-acquire the media from the swarm.

---

## Project Status: Alpha
**Warning:** This software is experimental and **Work in Progress**. It is not recommended for production use. Any and all code is subject to radical changes as development progresses.

---

## Installation

### 1. pip

* Install with [pip](https://pypi.org/project/backuparr/) _(requires a virtual environment)_:
    ```
    pip install backuparr
    ```

### 2. pipx (Recommended)

* Install with pipx, this requires pipx to be installed. See [pipx wiki](https://pipx.pypa.io/stable/how-to/install-pipx/).
    ```
    pipx install backuparr
    ```

---

## First Setup

* **Running First Config Setup:**
    ```
    backuparr-init
    ```
    This will copy the .env.example file to the .env file, and will ask for the initial values of the keys.

---

## Usage

* **Changing environment variables**
    ```
    backuparr-config
    ```
   This will allow you to change the environment variables via the cmd.


* **Command Structure:**
    ```bash
    backuparr [backup|restore] [radarr|sonarr] [filename].json
* **Example Command:**
    ```bash
    backuparr backup radarr radarr_backup.json
    ```

---

## Contributing
We welcome all input during these early stages!
* Open an **Issue** to discuss new ideas or report bugs.
* Submit a **Pull Request** to help with early-stage logic.
* Check the **Discussions** tab to help define the project roadmap.

---

## Development

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/DanielMayhan/BackupArr.git
    cd BackupArr/backuparr
    ```

2.  **Configure Environment:**
    Copy the sample configuration and add your Radarr & Sonarr Api Keys.
    ```bash
    cp .env.example .env
    ```
    
---

## Roadmap
These are features and code changes that are either currently being worked on or are planned to be implemented later!
* Unification of all text in-/outputs
* Better integration for automated Backups
* More Installation Methods


---

## License
This project is licensed under the [MIT License](LICENSE).
