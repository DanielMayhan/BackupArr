import os

import requests

radarr_apikey = str(os.getenv("API_KEY"))

def getmagnetlink(id):
    data = requests.get("http://127.0.0.1:7878/api/v3/history/movie?movieId=" + str(id) + "&eventType=grabbed&includeMovie=false&apiKey=" + radarr_apikey).json()
    return data[0]["data"]["downloadUrl"]