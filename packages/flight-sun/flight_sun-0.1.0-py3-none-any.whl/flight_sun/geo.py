import math
from datetime import datetime, timedelta, timezone
import skyfield.api
from typing import Generator


class Coordinate:
    def __init__(self, latitude: float, longitude: float):
        self.latitude = latitude
        self.longitude = longitude

    def __str__(self):
        return f"({self.latitude}, {self.longitude})"

    def path_to(self, other: "Coordinate", steps: int) -> list["Coordinate"]:
        return great_circle_path(self, other, steps)


class TimedCoordinate:
    def __init__(self, coordinate: Coordinate, time: datetime):
        self.coordinate = coordinate
        self.time = time

    def __str__(self):
        return f"({self.coordinate}, {self.time})"


def great_circle_distance(origin: Coordinate, destination: Coordinate) -> float:
    radius = 6371000 # Radius of the earth in metres

    lat_1 = math.radians(origin.latitude)
    lat_2 = math.radians(destination.latitude)
    d_lat = math.radians(origin.latitude - destination.latitude)
    d_lon = math.radians(origin.longitude - destination.longitude)

    a = (math.sin(d_lat / 2) ** 2) + math.cos(lat_1) * math.cos(lat_2) * (math.sin(d_lon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c

    return d


def great_circle_intermediate_point(origin: Coordinate, destination: Coordinate, fraction: float) -> Coordinate:
    lat_1, lat_2, lon_1, lon_2 = map(math.radians, [origin.latitude, destination.latitude, origin.longitude, destination.longitude])

    d = great_circle_distance(origin, destination) / 6371000

    a = math.sin((1 - fraction) * d) / math.sin(d)
    b = math.sin(fraction * d) / math.sin(d)

    x = a * math.cos(lat_1) * math.cos(lon_1) + b * math.cos(lat_2) * math.cos(lon_2)
    y = a * math.cos(lat_1) * math.sin(lon_1) + b * math.cos(lat_2) * math.sin(lon_2)
    z = a * math.sin(lat_1) + b * math.sin(lat_2)

    lat = math.atan2(z, math.sqrt(x ** 2 + y ** 2))
    lon = math.atan2(y, x)

    return Coordinate(math.degrees(lat), math.degrees(lon))


def great_circle_path(origin: Coordinate, destination: Coordinate, steps: int) -> list[Coordinate]:
    path = []

    for i in range(steps):
        path.append(great_circle_intermediate_point(origin, destination, i / steps))

    path.append(destination)

    return path


def timed_great_circle_path(origin: Coordinate, destination: Coordinate, origin_time: datetime, destination_time: datetime, interval: timedelta = timedelta(minutes=1)) -> list[TimedCoordinate]:
    if destination_time < origin_time:
        raise ValueError("Destination time must be after origin time")

    # Convert times to UTC, and store as timezone aware datetimes
    origin_time_utc = origin_time.astimezone(timezone.utc)
    destination_time_utc = destination_time.astimezone(timezone.utc)

    steps = int((destination_time_utc - origin_time_utc) / interval)

    path = great_circle_path(origin, destination, steps)

    time_delta = (destination_time_utc - origin_time_utc) / steps

    time_points = [origin_time_utc + time_delta * i for i in range(steps + 1)]

    return [TimedCoordinate(path[i], time_points[i]) for i in range(steps + 1)]


class SunlightSegment:

    def __init__(self, sun_up: bool, start: datetime, end: datetime, coordinates: list[TimedCoordinate]):
        self.sun_up = sun_up
        self.start = start
        self.end = end
        self.time_delta = end - start
        self.coordinates = coordinates

    def __str__(self):
        return f"SunlightSegment(sun_up={self.sun_up}, start={self.start}, end={self.end}, time_delta={self.time_delta})"

    @staticmethod
    def from_timed_coordinates(coordinates: list[TimedCoordinate]) -> Generator["SunlightSegment", None, None]:
        if len(coordinates) == 0:
            return []
        # Arrange coordinates chronologically
        coordinates.sort(key=lambda x: x.time)
        altitude_calculator = AltitudeCalculator()
        sun_up = None
        start_time = None
        segment_coordinates = []
        for coordinate in coordinates:
            altitude = altitude_calculator.sun_altitude(coordinate.coordinate, coordinate.time)
            current_sun_up = bool(altitude > 0)
            segment_coordinates.append(coordinate)
            if sun_up is None:
                sun_up = current_sun_up
                start_time = coordinate.time
            elif sun_up != current_sun_up:
                yield SunlightSegment(sun_up, start_time, coordinate.time, coordinates)
                sun_up = current_sun_up
                start_time = coordinate.time
        yield SunlightSegment(sun_up, start_time, coordinates[-1].time, coordinates)


class AltitudeCalculator:
    """
    Utility class for calculating altitude of the sun at a given position and time.
    Caches Skyfield objects to improve performance when calculating altitude for multiple positions and times.
    """
    def __init__(self):
        self.ts = skyfield.api.load.timescale()
        planets = skyfield.api.load('de421.bsp')
        self.earth, self.sun = planets['earth'], planets['sun']

    def sun_altitude(self, position: Coordinate, time: datetime) -> float:
        """
        Returns the sun's altitude at a given position and time.
        """
        t = self.ts.from_datetime(time)
        location = self.earth + skyfield.api.wgs84.latlon(position.latitude, position.longitude)
        astrometric = location.at(t).observe(self.sun).apparent()
        alt, _, _ = astrometric.altaz()
        return alt.degrees