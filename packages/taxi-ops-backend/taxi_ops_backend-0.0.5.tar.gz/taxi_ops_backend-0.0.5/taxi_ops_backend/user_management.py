"""This is the service layer which is exposed using API gateway.
This should go in lambda
"""
from src.taxi_ops_backend.database_management import DatabaseManagement


def register_user(name, email_id, phone_number) -> str:
    """
    doc string
    :param name:
    :param email_id:
    :param phone_number:
    :return:
    """
    return DatabaseManagement().create_user(user_name=name,
                                            email_id=email_id,
                                            phone_number=phone_number)
