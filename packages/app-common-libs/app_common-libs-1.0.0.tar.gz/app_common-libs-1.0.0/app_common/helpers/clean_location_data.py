import copy
import os

import requests

# GOOGLE API KEY need to move in environment variables
from app_common.config.base import IS_PROD

GOOGLE_API_KEY = os.environ.get('google_api_key')
SNAP_TO_ROAD_API = f"""
https://roads.googleapis.com/v1/snapToRoads?path=-%s&interpolate=true&key={GOOGLE_API_KEY}
"""


def clean_location_data(data):
    # Clean location data only in production environment
    if IS_PROD:
        batch_size = 100
        cleaned_data = []
        chunks_number = int(len(data) / batch_size) + 1
        for chunk_n in range(0, chunks_number):
            offset = chunk_n * batch_size
            json_data = data[offset:(offset + batch_size)]
            snapped_data = snap_to_road(json_data)
            cleaned_data.extend(snapped_data)
        print('cleaned data:-', cleaned_data)
        return cleaned_data
    else:
        return clean_stag_data(data)


def snap_to_road(json_data):
    print('Raw data:-', json_data)
    path = [f'{location.get("latitude")},{location.get("longitude")}' for location in
            json_data]
    path = '|'.join(path)
    api_end_point = SNAP_TO_ROAD_API % path
    response = requests.get(url=api_end_point)
    data = response.json()
    print('Snapped data:-', data)
    snapped_locations = data.get('snappedPoints')
    cleaned_locations = []
    index_location = None
    for location in snapped_locations:
        original_index = location.get('originalIndex')
        if original_index:
            index_location = json_data[original_index]
        if index_location:
            location_coord = location.get('location', {})
            existing_location = copy.deepcopy(index_location)
            map_keys(existing_location)
            existing_location['latitude'] = location_coord.get(
                'latitude', existing_location['latitude']
            )
            existing_location['longitude'] = location_coord.get(
                'longitude', existing_location['longitude']
            )
            existing_location['place_id'] = location.get('placeId')
            cleaned_locations.append(existing_location)
    return cleaned_locations


def clean_stag_data(data):
    for location in data:
        map_keys(location)
    return data


def map_keys(location):
    location['driver_id'] = location.pop('driverId', location.get('driver_id'))
    location['campaign_id'] = location.pop('campaignId', location.get('campaign_id'))
