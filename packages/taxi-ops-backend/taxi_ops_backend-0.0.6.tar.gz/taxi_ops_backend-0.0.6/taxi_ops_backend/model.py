"""Data model to used in this project"""

import datetime
from dataclasses import dataclass
from typing import Optional
from dataclasses_json import dataclass_json
from geojson import Point


@dataclass_json
@dataclass
class User:
    """User Table"""
    # attributes
    name: str
    email_id: str
    phone_number: str
    location: Optional[Point] = None
    # will work out: user_id remains blank in DB
    user_id: Optional[str] = ""


@dataclass_json
@dataclass
class Driver:
    """Driver Table"""
    driver_name: str
    email_id: str
    phone_number: str
    status: Optional[str] = "OFF DUTY"
    taxi_assigned: Optional[bool] = False
    location: Optional[Point] = None
    # will work out: driver_id remains blank in DB
    driver_id: Optional[str] = ""


TaxiType = ["Utility", "Deluxe", "Luxury"]
TaxiStatus = ["Not Operational", "Occupied", "Available"]


@dataclass
class Taxi:
    """Taxi table"""
    taxi_type: str
    taxi_number: str
    status: str
    location: Point
    # Assumption for this project is that there would be 1 driver for a taxi
    driver_id: Optional[str] = ""
    # will work out: taxi_id remains blank in DB
    taxi_id: Optional[str] = ""

    def to_dict(self):
        """converts taxi object to dict"""
        geojson_point = None
        if self.location is not None:
            # geojson_point = {"type": "Point", "coordinates": self.location["coordinates"][0]}
            geojson_point = self.location["coordinates"][0]

        return {"taxi_type": self.taxi_type, "taxi_number": self.taxi_number,
                "status": self.status, "driver_id": self.driver_id,
                "location": geojson_point}


@dataclass_json
@dataclass
class OperationBoundary:
    """Operation Boundary"""
    city: str
    location: list[(float, float)]


TripStatus = ["Not Started", "In Progress", "Completed"]


@dataclass
class TripInfo:
    """TripInfo Table"""
    trip_id: str
    user_id: str
    taxi_id: str
    starting_point: Point
    destination_point: Point
    status: TripStatus
    start_time: Optional[datetime.datetime] = None
    end_time: Optional[datetime.datetime] = None

    @staticmethod
    def point_to_location(point):
        """
        geojson point to mongodb compatible location
        @param point:
        @return:
        """
        geojson_point = None
        if point is not None:
            geojson_point = point["coordinates"]
        return geojson_point

    def to_dict(self):
        """converts trip info into dict"""
        return {"trip_id": self.trip_id, "user_id": self.user_id,
                "taxi_id": self.taxi_id,
                "starting_point": self.point_to_location(self.starting_point),
                "destination_point": self.point_to_location(self.destination_point),
                "status": self.status, "start_time": self.start_time,
                "end_time": self.start_time}


@dataclass
class TripInfoDetail:
    """TripInfoDetail Table"""
    trip_id: str
    location: Point
    reporting_time: datetime.datetime
    expected_time_for_completion_in_min: int

    def to_dict(self):
        """converts taxi object to dict"""
        geojson_point = None
        if self.location is not None:
            geojson_point = self.location["coordinates"]

        return {"trip_id": self.trip_id, "location": geojson_point,
                "reporting_time": self.reporting_time,
                "expected_time_for_completion_in_min":
                    self.expected_time_for_completion_in_min}
