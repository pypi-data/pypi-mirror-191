"""
Taxi Administration. This is to be run on EC2 machine because this is
helper to the taxi ops
"""
import random

from .custom_error import IllegalTaxiStatusState
from .database_management import DatabaseManagement
from .taxi_ops_logger import TaxiOpsLogger
from .model import Taxi


def register_taxi(taxi_type, taxi_number):
    """
    doc string
    :param taxi_type:
    :param taxi_number:
    :return:
    """
    return DatabaseManagement().create_taxi(taxi_type=taxi_type, taxi_number=taxi_number)


def register_driver(driver_name, email_id, phone_number) -> str:
    """
    doc string
    :param driver_name:
    :param email_id:
    :param phone_number:
    :return:
    """
    return DatabaseManagement().create_driver(driver_name=driver_name,
                                              email_id=email_id,
                                              phone_number=phone_number)


def register_drivers_with_taxis():
    """registers driver with taxi
    :return: None
    """
    logger = TaxiOpsLogger()
    # get the required list of taxi and driver.
    unallocated_taxis = DatabaseManagement().get_taxis({"driver_id": ""})
    unallocated_drivers = DatabaseManagement().get_drivers({"taxi_assigned": False})

    # just randomise to be fair
    random.shuffle(unallocated_taxis)
    random.shuffle(unallocated_drivers)

    # now assign
    while len(unallocated_drivers) > 0 and len(unallocated_taxis) > 0:
        taxi = unallocated_taxis.pop(0)
        driver = unallocated_drivers.pop(0)
        driver.taxi_assigned = True
        taxi.driver_id = driver.driver_id
        logger.info("Now registering taxi: %s with driver: %s",
                    taxi.taxi_number,
                    driver.driver_name)

        success = False
        retry = 0
        while not success and retry < 3:
            success = DatabaseManagement().register_driver_with_taxi(driver=driver,
                                                                     taxi=taxi)
            retry += 1
        logger.info("Registration Result: %s", success)


def set_taxi_available(taxi_id) -> bool:
    """get available taxis"""
    return DatabaseManagement().update_taxi_status(taxi_id, "Available")


def get_available_taxis() -> list[Taxi]:
    """get available taxis"""
    return DatabaseManagement().get_taxis({"status": "Available"})


def get_taxi_current_status(taxi_id) -> str:
    """get taxi current status"""
    return DatabaseManagement().get_taxi_current_status(taxi_id=taxi_id)


def set_taxis_drivers_ready():
    """Per design, Driver make taxi available when he is ON-DUTY. Taxi should always emit
     location when it is available.
     This function is a series of helper procedure:
         1. The driver gets active - his status gets to ON DUTY
         2. The car becomes available and starts emitting its locations"""
    logger = TaxiOpsLogger()
    driver_list = DatabaseManagement().get_drivers(({}))
    taxi_list = DatabaseManagement().get_taxis(({}))
    taxi_dict: dict[str, Taxi] = {}
    for taxi in taxi_list:
        taxi_dict[taxi.driver_id] = taxi

    for driver in driver_list:
        b_success = DatabaseManagement().update_driver_status(driver_id=driver.driver_id,
                                                              status="ON-DUTY")
        if b_success:
            taxi = taxi_dict[driver.driver_id]
            logger.info("Driver - %s tagged with taxi %s status ON-DUTY: %s",
                        driver.driver_name, taxi.taxi_number, str(b_success))
            b_success = DatabaseManagement().update_taxi_status(taxi_id=taxi.taxi_id,
                                                                status="Available")
            logger.info("Associated taxi - %s status Available: %s", taxi.taxi_number,
                        str(b_success))

    logger.info("***All taxis and driver ready**** Refreshed list")
    taxi_list = DatabaseManagement().get_taxis(({}))
    logger.info(taxi_list)


def find_nearest_taxi(current_location, max_distance, max_number_of_taxi) -> list:
    """
    find the nearest taxi
    @param current_location:
    @param max_distance:
    @param max_number_of_taxi:
    @return:
    """
    return DatabaseManagement().find_nearest_taxi(current_location,
                                                  max_distance,
                                                  max_number_of_taxi)


def update_taxi_location(v_taxi_id, v_location):
    """
    update taxi location
    @param v_taxi_id:
    @param v_location:
    @return:
    """
    logger = TaxiOpsLogger()
    DatabaseManagement().update_taxi_location(v_taxi_id, v_location)
    logger.info("Taxi movement to %s - completed", v_location)


def book_and_initiate_trip(taxi_id, user_id, current_location, destination_location):
    """
    book_and_initiate_trip
    @param taxi_id:
    @param user_id:
    @param current_location:
    @param destination_location:
    @return:
    """
    # mark taxi_id status and Occupied.
    # Check if taxi_is current state is Available, If so, mark it Occupied. If not, send error
    logger = TaxiOpsLogger()
    current_status = DatabaseManagement().get_taxi_current_status(taxi_id)
    if current_status != "Available":
        raise IllegalTaxiStatusState(f"Taxi has already become {current_status}")

    b_success = DatabaseManagement().update_taxi_status(taxi_id, "Occupied")
    if b_success:
        trip_id = DatabaseManagement().create_trip(taxi_id, user_id,
                                                   current_location, destination_location)
        logger.info("Trip created - %s", trip_id)
        logger.info("Taxi moving to user location...")
        DatabaseManagement().update_taxi_location(taxi_id, current_location)
        logger.info("Taxi movement to %s - completed", current_location)

        b_success = DatabaseManagement().mark_trip_in_progress(trip_id=trip_id)
        if b_success:
            logger.info("Marking trip - %s in progress", trip_id)
            return trip_id, b_success
        return trip_id, b_success
    return None, False


def insert_trip_info_detail(trip_id, location, expected_time_for_completion):
    """
    insert trip info detail
    @param trip_id:
    @param location:
    @param expected_time_for_completion:
    @return:
    """
    return DatabaseManagement() \
        .insert_trip_location(trip_id=trip_id,
                              location=location,
                              eta=expected_time_for_completion)
