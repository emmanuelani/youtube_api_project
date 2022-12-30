import json
import pandas as pd

from googleapiclient.discovery import build 

# setting up the API
api_key = "AIzaSyDxZqdVOLAs7gHhVg3iMi_IXSOU4OpuF7o"
api_service_name="youtube"
api_version="v3"

youtube = build(
    api_service_name,
    api_version,
    developerKey="AIzaSyDxZqdVOLAs7gHhVg3iMi_IXSOU4OpuF7o"
)

request= youtube.channels().list(
    part="contentDetails, statistics",
    forUsername="schafer5"
)

response = request.execute()

print(json.dumps(response, indent=2))