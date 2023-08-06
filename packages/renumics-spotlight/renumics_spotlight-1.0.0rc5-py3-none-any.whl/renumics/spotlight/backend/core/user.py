"""
user core commands
"""
from datetime import date
from typing import Optional
from pydantic import BaseModel  # pylint: disable=no-name-in-module

from renumics.spotlight.licensing import LicensedFeature

# pylint: disable=too-few-public-methods
class User(BaseModel):
    """
    a User
    """

    user_name: str
    expiration_date: date
    row_limit: Optional[int]
    column_limit: Optional[int]
    has_test_license: bool


def get_user(spotlight_license: LicensedFeature) -> User:
    """
    read user from license file and return it
    """

    return User(
        user_name=spotlight_license.users[0],
        expiration_date=spotlight_license.expiration_date,
        row_limit=spotlight_license.row_limit,
        column_limit=spotlight_license.column_limit,
        has_test_license=spotlight_license.is_test,
    )
