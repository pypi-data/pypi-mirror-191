"""Renumics Licensing"""
import os
import sys
from pathlib import Path

from loguru import logger

from .terms_and_conditions import (
    TermsAndConditionsNotAccepted,
    verify_terms_and_conditions,
)
from .verification import FeatureNotLicensed, LicensedFeature, verify_feature


# Search for SPOTLIGHT_LICENSE_PATH environment variable,
# if not found, take ./renumics_license.key.
license_path = (
    Path(
        next(
            (v for k, v in os.environ.items() if k.upper() == "SPOTLIGHT_LICENSE_PATH"),
            "renumics_license.key",
        )
    )
    .expanduser()
    .resolve()
)


def verify_license_or_exit() -> LicensedFeature:
    """
    Check if Renumics license is valid.
    Otherwise, close Spotlight.
    """
    try:
        return verify_feature("spotlight", license_path)
    except FeatureNotLicensed as e:
        logger.error(e)
        sys.exit(1)


def verify_terms_and_conditions_or_exit() -> None:
    """
    Force to accept Renumics Spotlight terms and conditions.
    Otherwise, close Spotlight.
    """
    try:
        verify_terms_and_conditions()
    except TermsAndConditionsNotAccepted as e:
        logger.error(e)
        sys.exit(1)


spotlight_license = verify_license_or_exit()
verify_terms_and_conditions_or_exit()
username = spotlight_license.users[0]
