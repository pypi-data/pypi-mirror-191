"""This is the service layer which is exposed using API gateway.
This should go in lambda
"""
from src.taxi_ops_backend.database_management import DatabaseManagement


def define_boundary_location(city: str,
                             left_bottom: (float, float),
                             left_top: (float, float),
                             right_top: (float, float),
                             right_bottom: (float, float)):
    """
    define city operation boundary
    @param city:
    @param left_bottom:
    @param left_top:
    @param right_top:
    @param right_bottom:
    @return:
    """
    return DatabaseManagement().create_operation_bound(city, left_bottom,
                                                       left_top,
                                                       right_top,
                                                       right_bottom)


def get_operation_boundary(city):
    """
    get operation boundary polygon
    @param city:
    @return:
    """
    return DatabaseManagement().get_operation_bound(city=city)
