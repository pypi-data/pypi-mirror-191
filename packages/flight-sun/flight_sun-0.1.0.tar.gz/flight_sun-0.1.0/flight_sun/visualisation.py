from typing import List
from flight_sun.geo import SunlightSegment

def generate_geojson(segments: List[SunlightSegment]) -> dict:
    """
    Generate a GeoJSON object from a list of SunlightSegments.
    Includes a property for whether the segment is in sunlight.
    """
    features = []
    # Each segment is a separate LineString feature
    for segment in segments:
        # Create coordinate line string
        coordinates = [[coordinate.coordinate.longitude, coordinate.coordinate.latitude] for coordinate in segment.coordinates]
        # Create feature
        feature = {
            "type": "Feature",
            "properties": {
                "sun_up": segment.sun_up
            },
            "geometry": {
                "type": "LineString",
                "coordinates": coordinates
            }
        }
        features.append(feature)
    # Create GeoJSON object
    return {
        "type": "FeatureCollection",
        "features": features
    }
