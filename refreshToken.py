from SpotifySecret import refresh_token, base_64
import requests
import json

class Refresh:

    def _init_(self):
        self.refresh_token = refresh_token
        self.base_64 = base_64

    def refresh(self):
        #curl - H "Authorization: Basic ZjM...zE=" - d grant_type = authorization_code - d code = MQCbtKe...44KN - d redirect_uri = https % 3A % 2F % 2Fwww.foo.com % 2Fauth https://accounts.spotify.com/api/token

        query = "https://accounts.spotify.com/api/token"

        response = requests.post(query, data={"grant_type": "refresh_token", "refresh_token": refresh_token}, headers={"Authorization": "Basic " + base_64})
        print("test")

        response_json = response.json()

        return response_json["access_token"]
