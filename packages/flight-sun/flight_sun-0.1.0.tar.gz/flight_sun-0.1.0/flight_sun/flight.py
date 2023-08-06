from datetime import datetime
from flight_sun.geo import Coordinate, timed_great_circle_path, SunlightSegment
from functools import cached_property
import airportsdata
from zoneinfo import ZoneInfo


class Flight:

    def __init__(self, origin: Coordinate, destination: Coordinate, departure: datetime, arrival: datetime):
        self.origin = origin
        self.destination = destination
        self.departure = departure
        self.arrival = arrival
        self.path = timed_great_circle_path(origin, destination, departure, arrival)
        self.duration = arrival - departure

    @cached_property
    def light_segments(self) -> list[SunlightSegment]:
        return list(SunlightSegment.from_timed_coordinates(self.path))

    def proportion_in_sunlight(self) -> float:
        """
        Returns the proportion of the flight path that is in sunlight.
        """
        total_time = (self.arrival - self.departure).total_seconds()
        sun_up_segments = [segment for segment in self.light_segments if segment.sun_up]
        total_sunlight = sum([segment.time_delta.total_seconds() for segment in sun_up_segments])
        return total_sunlight / total_time

    def __str__(self):
        return f"Flight(origin={self.origin}, destination={self.destination}, departure={self.departure}, arrival={self.arrival}, duration={self.duration})"

    @staticmethod
    def between_airports(origin_airport: dict, destination_airport: dict, departure: datetime, arrival: datetime) -> "Flight":
        # Check if datetimes are timezone-aware
        if departure.tzinfo is None:
            departure = departure.replace(tzinfo=ZoneInfo(origin_airport['tz']))
        if arrival.tzinfo is None:
            arrival = arrival.replace(tzinfo=ZoneInfo(destination_airport['tz']))
        origin_coordinate = Coordinate(origin_airport['lat'], origin_airport['lon'])
        destination_coordinate = Coordinate(destination_airport['lat'], destination_airport['lon'])
        return Flight(origin_coordinate, destination_coordinate, departure, arrival)

    @staticmethod
    def from_iata_codes(origin_iata: str, destination_iata: str, departure: datetime, arrival: datetime):
        """
        Create a flight from IATA codes.
        If timezone-naive datetimes are provided, they will be converted to local time.

        :param origin_iata: IATA code of origin airport
        :param destination_iata: IATA code of destination airport
        :param departure: departure time
        :param arrival: arrival time
        :return: Flight object
        """
        iata_data = airportsdata.load("IATA")
        if origin_iata not in iata_data.keys():
            raise ValueError(f"Invalid IATA code: {origin_iata}")
        if destination_iata not in iata_data.keys():
            raise ValueError(f"Invalid IATA code: {destination_iata}")
        return Flight.between_airports(iata_data[origin_iata], iata_data[destination_iata], departure, arrival)

    @staticmethod
    def from_icao_codes(origin_icao: str, destination_icao: str, departure: datetime, arrival: datetime):
        """
        Create a flight from ICAO codes.
        If timezone-naive datetimes are provided, they will be converted to local time.

        :param origin_icao: ICAO code of origin airport
        :param destination_icao: ICAO code of destination airport
        :param departure: departure time
        :param arrival: arrival time
        :return: Flight object
        """
        icao_data = airportsdata.load("ICAO")
        if origin_icao not in icao_data.keys():
            raise ValueError(f"Invalid ICAO code: {origin_icao}")
        if destination_icao not in icao_data.keys():
            raise ValueError(f"Invalid ICAO code: {destination_icao}")
        return Flight.between_airports(icao_data[origin_icao], icao_data[destination_icao], departure, arrival)

