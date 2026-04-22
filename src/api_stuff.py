import os
from enum import Enum

__internal_radarr_apikey__ = str(os.getenv("API_KEY"))

class radarrapi(str, Enum):
    apikey = "apiKey=" + str(__internal_radarr_apikey__)
    baseurl = "http://127.0.0.1:7878"
    movieListUrl = baseurl + "/api/v3/movie" + "?" + apikey
    qualityProfileUrl = baseurl + "/api/v3/qualityprofile" + "?" + apikey
    rootFolderUrl = baseurl + "/api/v3/rootfolder" + "?" + apikey