import os
from enum import StrEnum

from dotenv import load_dotenv

load_dotenv()

class radarr(StrEnum):
    apiKey = str(os.getenv("RADARR_APIKEY"))
    baseUrl = str(os.getenv("RADARR_URL"))
    movieListUrl = baseUrl + "/api/v3/movie"
    qualityProfileUrl = baseUrl + "/api/v3/qualityprofile"
    rootFolderUrl = baseUrl + "/api/v3/rootfolder"

class sonarr(StrEnum):
    apiKey = str(os.getenv("SONARR_APIKEY"))
    baseUrl = str(os.getenv("SONARR_URL"))
    seriesListUrl = baseUrl + "/api/v3/series"
    episodeFileUrl = baseUrl + "/api/v3/episodefile"