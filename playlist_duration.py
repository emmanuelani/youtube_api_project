import json
import re
from datetime import timedelta

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

hours_pattern = re.compile(r"([0-9]+)H")
minutes_pattern = re.compile(r"([0-9]+)M")
seconds_pattern = re.compile(r"([0-9]+)S")

total_seconds = 0

nextPageToken = None
while True:
    pl_request= youtube.playlistItems().list(
        part="contentDetails",
        playlistId="PL-osiE80TeTsKOdPrKeSOp4rN3mza8VHN",
        maxResults=50,
        pageToken=nextPageToken
    )

    pl_response = pl_request.execute()

    # print(pl_response)
    # print(json.dumps(pl_response, indent=2))
    vid_ids = []

    for item in pl_response["items"]:
        vid_ids.append(item['contentDetails']['videoId'])

    vid_id_string = ','.join(vid_ids)  

    # sending a new requests 
    vid_request = youtube.videos().list(
        part="contentDetails, statistics",
        id=vid_id_string,
    )

    vid_response = vid_request.execute()

    for item in vid_response["items"]:
        duration = item["contentDetails"]["duration"]
        hours = hours_pattern.search(duration)
        minutes = minutes_pattern.search(duration)
        seconds = seconds_pattern.search(duration)
        
        hours = int(hours.group(1)) if hours else 0
        minutes = int(minutes.group(1)) if minutes else 0
        seconds = int(seconds.group(1)) if seconds else 0
        
        video_seconds = timedelta(
            hours = hours,
            minutes = minutes,
            seconds = seconds
        ).total_seconds()
        
        total_seconds += video_seconds
        
    nextPageToken = pl_response.get("nextPageToken")
    
    if not nextPageToken:
        break
    
total_seconds = int(total_seconds)

minutes, seconds = divmod(total_seconds, 60)

hours, minutes = divmod(minutes, 60)

print(f"{hours}:{minutes}:{seconds}")