"""
Wrapper class over DB operations
"""
from datetime import datetime

from bson import ObjectId
from geojson import Point

from .database import Database
from .model import User, Taxi, Driver, OperationBoundary, TripInfo, TripInfoDetail
from .taxi_ops_logger import TaxiOpsLogger


class DatabaseManagement:
    """
    Class doc string
    """

    def __init__(self):
        """
        Init Doc string
        """
        self._database = Database()
        self._logger = TaxiOpsLogger()

    def create_user(self, user_name, email_id, phone_number) -> str:
        """
        Makes an entry in User data
        :param user_name:
        :param email_id:
        :param phone_number:
        :return:
        """
        user: User = User(user_name, email_id, phone_number)
        return self._database.insert_single_data(collection="Users",
                                                 data=user.to_dict())  # pylint: disable=no-member

    def create_taxi(self, taxi_type, taxi_number) -> str:
        """
        Makes an entry in Taxis table
        :param taxi_type: taxi type
        :param taxi_number: taxi number
        :return: Object(_id) string
        """
        taxi: Taxi = Taxi(taxi_type=taxi_type, taxi_number=taxi_number, status="Not Operational",
                          location=Point([(0, 0)]))
        return self._database.insert_single_data(collection="Taxis",
                                                 data=taxi.to_dict(),  # pylint: disable=no-member
                                                 index_key="location")

    # driver
    def create_driver(self, driver_name, email_id, phone_number) -> str:
        """
        doc string
        :param driver_name:
        :param email_id:
        :param phone_number:
        :return:
        """
        driver: Driver = Driver(driver_name=driver_name,
                                email_id=email_id,
                                phone_number=phone_number)
        return self._database.insert_single_data(collection="Drivers",
                                                 data=driver.to_dict())  # pylint: disable=no-member

    def get_taxis(self, taxi_filter):
        """
        Gets all the drivers as per filter. In case, all is required, pass empty filter
        @param taxi_filter:
        @return:
        """
        taxi_documents = self._database.find_multiple("Taxis", taxi_filter)
        taxi_list = []
        for taxi_document in taxi_documents:
            taxi = Taxi(taxi_type=taxi_document['taxi_type'],
                        taxi_number=taxi_document['taxi_number'],
                        status=taxi_document['status'],
                        driver_id=taxi_document['driver_id'],
                        location=taxi_document['location'],
                        taxi_id=str(taxi_document['_id']))
            taxi_list.append(taxi)
        return taxi_list

    def get_drivers(self, driver_filter):
        """
        Gets all the drivers as per filter. In case, all is required, pass empty filter
        @param driver_filter:
        @return:
        """
        driver_documents = self._database.find_multiple("Drivers", driver_filter)
        driver_list = []
        for driver_document in driver_documents:
            driver = Driver(driver_name=driver_document['driver_name'],
                            email_id=driver_document['email_id'],
                            phone_number=driver_document['phone_number'],
                            status=driver_document["status"],
                            taxi_assigned=driver_document['taxi_assigned'],
                            location=driver_document['location'],
                            driver_id=str(driver_document['_id']))
            driver_list.append(driver)
        return driver_list

    def register_driver_with_taxi(self, driver: Driver, taxi: Taxi) -> bool:
        """
        update taxi with driver_id and mark driver as taxi_assigned.
        :param driver:
        :param taxi:
        :return:
        """
        matched_count, modified_count = \
            self._database.update_single("Taxis",
                                         {"_id": ObjectId(taxi.taxi_id)},
                                         {"$set": {'driver_id': taxi.driver_id}})
        self._logger.info("Taxi %s record Update: matched: %s and modified: %s",
                          taxi.taxi_number, matched_count, modified_count)
        if matched_count == modified_count == 1:
            matched_count, modified_count = \
                self._database.update_single("Drivers",
                                             {"_id": ObjectId(driver.driver_id)},
                                             {"$set": {'taxi_assigned': driver.taxi_assigned}})
            self._logger.info("Driver %s record Update: matched: %s and modified: %s",
                              driver.driver_name, matched_count, modified_count)

        self._logger.info("Taxi: %s is allocated to driver %s",
                          taxi.taxi_number, driver.driver_name)
        return matched_count == modified_count == 1
        # self._database.run_as_transactions(func_list)

    def get_taxi_current_status(self, taxi_id):
        """
        doc string
        :param taxi_id:
        :return:
        """
        taxi = self._database.find_one("Taxis", {"_id": ObjectId(taxi_id)})
        return taxi['status']

    def update_taxi_status(self, taxi_id, status) -> bool:
        """
        doc string
        :param taxi_id:
        :param status:
        :return:
        """
        matched_count, modified_count = self._database \
            .update_single(collection="Taxis",
                           update_filter={"_id": ObjectId(taxi_id)},
                           update={"$set": {'status': status}})
        return matched_count == modified_count == 1

    def update_driver_status(self, driver_id, status) -> bool:
        """
        doc string
        :param driver_id:
        :param status:
        :return:
        """
        matched_count, modified_count = self._database \
            .update_single(collection="Drivers",
                           update_filter={"_id": ObjectId(driver_id)},
                           update={"$set": {'status': status}})
        return matched_count == modified_count == 1

    def get_current_driver(self, taxi_id):
        """
        doc string
        :param taxi_id:
        :return:
        """

    def get_user_booking(self, user_id):
        """
        doc string
        :param user_id:
        :return:
        """

    def create_operation_bound(self, city,
                               left_bottom: (float, float),
                               left_top: (float, float),
                               right_top: (float, float),
                               right_bottom: (float, float)):
        """
        create operation boundary for city
        @param city:
        @param left_bottom:
        @param left_top:
        @param right_top:
        @param right_bottom:
        @return:
        """
        polygon = [left_bottom, left_top, right_top, right_bottom]
        operational_boundary = OperationBoundary(city, polygon)
        self._logger.info("Inserting Operational Boundary - %s",
                          operational_boundary.to_dict())  # pylint: disable=no-member
        return self._database.insert_single_data("Operation_Boundary",
                                                 operational_boundary.to_dict())  # pylint: disable=no-member

    def get_operation_bound(self, city):
        """
        get operation boundary
        @param city:
        @return:
        """
        document = self._database.find_one("Operation_Boundary", {"city": city})
        polygon_coordinates = document["location"]
        self._logger.info("Fetched polygon for %s - %s", city, polygon_coordinates)
        return polygon_coordinates

    def update_taxi_location(self, taxi_id, location) -> bool:
        """
        update taxi location
        @param taxi_id:
        @param location:
        @return:
        """
        matched_count, modified_count = self._database \
            .update_single(collection="Taxis",
                           update_filter={"_id": ObjectId(taxi_id)},
                           update={"$set": {
                               'location': location["coordinates"]
                           }
                           })
        return matched_count == modified_count == 1

    def find_nearest_taxi(self, current_location,
                          max_distance, max_number_of_taxi) -> list:
        """
        find the nearest taxi
        @param current_location:
        @param max_distance:
        @param max_number_of_taxi:
        @return:
        """
        longitude = current_location["coordinates"][0]
        latitude = current_location["coordinates"][1]
        documents = self._database \
            .find_nearest_entities_in_collection("Taxis",
                                                 longitude,
                                                 latitude,
                                                 max_distance,
                                                 max_number_of_taxi)
        taxi_list = []
        for taxi_document in documents:
            taxi = Taxi(taxi_type=taxi_document['taxi_type'],
                        taxi_number=taxi_document['taxi_number'],
                        status=taxi_document['status'],
                        driver_id=taxi_document['driver_id'],
                        location=taxi_document['location'],
                        taxi_id=str(taxi_document['_id']))
            taxi_list.append(taxi)

        return taxi_list

    def create_trip(self, taxi_id, user_id, current_location, destination_location) -> str:
        """
        create trip
        @param taxi_id:
        @param user_id:
        @param current_location:
        @param destination_location:
        @return:
        """
        trip_info = TripInfo(trip_id="", user_id=user_id, taxi_id=taxi_id,
                             starting_point=current_location,
                             destination_point=destination_location,
                             status="Not Started")
        self._logger.info("Now creating trip with details - ")
        self._logger.info(trip_info.to_dict())  # pylint: disable=no-member
        return self._database.insert_single_data("TripInfos", trip_info.to_dict())  # pylint: disable=no-member

    def mark_trip_in_progress(self, trip_id) -> bool:
        """

        @param trip_id:
        @return:
        """
        matched_count, modified_count = self._database \
            .update_single(collection="TripInfos",
                           update_filter={"_id": ObjectId(trip_id)},
                           update={"$set": {
                               "status": "In Progress",
                               "start_time": datetime.now()}})
        return matched_count == modified_count == 1

    def insert_trip_location(self, trip_id, location, eta):
        """
        insert new location
        @param trip_id:
        @param location:
        @param eta:
        @return:
        """
        trip_info_detail = TripInfoDetail(trip_id=trip_id,
                                          location=location,
                                          reporting_time=datetime.now(),
                                          expected_time_for_completion_in_min=eta)
        return self._database.insert_single_data(collection="TripInfoDetail",
                                                 data=trip_info_detail.to_dict())

    def clean_up_database(self):
        """clean up database"""
        for collection in ["Taxis", "Users", "Drivers", "Operation_Boundary",
                           "TripInfos", "TripInfoDetail"]:
            self._database.drop_collection(collection=collection)
        # for collection in ["Operation_Boundary"]:
        #     self._database.drop_collection(collection=collection)
