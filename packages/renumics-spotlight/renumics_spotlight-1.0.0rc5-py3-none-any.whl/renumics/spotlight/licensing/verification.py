"""this module can be copied to any renumics application to verify licensed feature"""
import getpass
import json
from base64 import b64decode
from dataclasses import dataclass, field
from datetime import date, timedelta
from pathlib import Path
from typing import List, Optional, Dict

import rsa
from packaging import version

from renumics.spotlight._build_variant import __build_variant__


@dataclass
class LicensedFeature:
    """contains information about a specific feature loaded form the license key"""

    name: str
    expiration_date_iso: str = "1900-01-01"
    max_version: str = "10.0.1"
    users: List[str] = field(default_factory=lambda: ["default_user"])
    is_test: bool = False
    row_limit: Optional[int] = None
    column_limit: Optional[int] = None

    @property
    def expiration_date(self) -> date:
        """the date string as date type"""
        return date.fromisoformat(self.expiration_date_iso)


CACHED_LICENSES: Dict[str, Dict[str, LicensedFeature]] = {}


class FeatureNotLicensed(Exception):
    """raised when feature fails the license verification"""


def verify_feature(
    feature_name: str,
    license_path: Path,
    current_feature_version: Optional[str] = None,
    public_key_path: Optional[Path] = None,
) -> LicensedFeature:
    """
    verify that the provided licens file allows a specific feature
    :param feature_name: the name of the feature the user wants to use
    :param license_path: the path to the users license file
    :param current_feature_version: the curret version of the feature implementation
    :return: license information about the feature - only if the feature allowed.
    """
    if __build_variant__ == "core":
        return LicensedFeature(
            feature_name,
            (date.today() + timedelta(365)).isoformat(),
            users=[getpass.getuser()],
        )
    public_key = _public_key(public_key_path)
    if str(license_path) in CACHED_LICENSES:
        features = CACHED_LICENSES[str(license_path)]
    else:
        features = _load_license_file(license_path, public_key)
        CACHED_LICENSES[str(license_path)] = features
    if feature_name not in features:
        raise FeatureNotLicensed(f"Feature {feature_name} is not licensed.")
    feature = features[feature_name]
    if feature.expiration_date < date.today():
        raise FeatureNotLicensed(
            f"Feature {feature_name} expired on {feature.expiration_date}."
        )
    if current_feature_version and version.parse(
        current_feature_version
    ) > version.parse(feature.max_version):
        if (
            not feature.max_version == "0.1"
        ):  # old license files having max_version=0.1 allow all versions.
            raise FeatureNotLicensed(
                f"Your license only allows to use versions up to {feature.max_version}. "
                f"Current feature version is {current_feature_version}. "
            )
    return feature


def _load_license_file(
    path: Path, public_key: rsa.PublicKey
) -> Dict[str, LicensedFeature]:
    if not path.is_file():
        raise FeatureNotLicensed(
            f"License File ({path.absolute()}) was not found or is not a file."
        )

    try:
        with open(path, encoding="utf-8") as license_file:
            signed_data = json.load(license_file)
    except Exception as e:
        raise FeatureNotLicensed(
            f"License file ({path.absolute()}) is not a valid JSON file."
        ) from e
    try:
        signature = b64decode(signed_data["signature"])
    except ValueError as e:
        raise FeatureNotLicensed(
            f"Signature of the license file ({path.absolute()}) is invalid."
        ) from e
    data_json = signed_data
    del data_json["signature"]
    signed_content = json.dumps(
        data_json,
        skipkeys=False,
        ensure_ascii=True,
        check_circular=True,
        allow_nan=True,
        cls=None,
        indent=None,
        separators=None,
        default=None,
        sort_keys=True,
    )
    try:
        rsa.verify(signed_content.encode("utf-8"), signature, public_key)
    except rsa.VerificationError as e:
        raise FeatureNotLicensed(
            "Signature verification error - license file was modified."
        ) from e
    features = {
        feature["name"]: LicensedFeature(**feature) for feature in data_json.values()
    }
    return features


def _public_key(path: Optional[Path] = None) -> rsa.key.PublicKey:
    if path:
        with open(path, "rb") as key_file:
            return rsa.key.PublicKey.load_pkcs1(key_file.read())  # type: ignore
    return rsa.key.PublicKey.load_pkcs1(
        b"""-----BEGIN RSA PUBLIC KEY-----
    MIIBigKCAYEAis0Tc10rWW3zWIW36slfPMqQueZRzZj2GvaC8f9VEvChR8ljo0Dr
    8YXW3Sa+ffawzOrIA2JTpmQ4a3GCNP6kCr0H1wIfuvcSCHGCKExnap4oVhFyK4/S
    +ZM7vd+kaWUHCqhl/e8WyrTH+kzPlwDZ1AhJAumwZfj9IkWJannWJQCGnOXkcP72
    v5etIiczDgQWEp63tXx9C23pi7WvNhpiHrxbDrTtpYa5kaNaR4vKI38qlcgKRuT9
    iFCy1iYu68MERLYdfxi7Hohl9+rrEiyMKHM92/i6VDBrZqe5oTeZVQBDEMB0dbkM
    mfGL1g+NhsjeeZ8IFDGke6bL5VBgS3gfaB5CRXvT/XOvCwQvLUfFTH2b20tvdLoc
    i4+l/sZm6oYlwrBHUA4CnI/Qjbsbo0gwZqnVWUuNZHT8AcQoBcFT7t+m9MDaH5pJ
    KDioxIAyUJFe3NNC0ZRP/sXcxFNDN4t5FHvocKKS6B61YKaQ70u7qvjAFS94hPUj
    vcajcFRBt93zAgMBAAE=
    -----END RSA PUBLIC KEY-----
    """
    )  # type: ignore
