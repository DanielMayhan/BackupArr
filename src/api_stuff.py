import os
from enum import StrEnum

class radarrapi(StrEnum ):
    apikey = "apiKey=" + str(os.getenv("RADARR_APIKEY"))
    baseurl = str(os.getenv("RADARR_URL"))
    movieListUrl = baseurl + "/api/v3/movie" + "?" + apikey
    qualityProfileUrl = baseurl + "/api/v3/qualityprofile" + "?" + apikey
    rootFolderUrl = baseurl + "/api/v3/rootfolder" + "?" + apikey