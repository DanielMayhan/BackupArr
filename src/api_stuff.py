import os
from enum import StrEnum

from dotenv import load_dotenv

load_dotenv()

class radarrapi(StrEnum ):
    apikey = str(os.getenv("RADARR_APIKEY"))
    baseurl = str(os.getenv("RADARR_URL"))
    movieListUrl = baseurl + "/api/v3/movie"
    qualityProfileUrl = baseurl + "/api/v3/qualityprofile"
    rootFolderUrl = baseurl + "/api/v3/rootfolder"