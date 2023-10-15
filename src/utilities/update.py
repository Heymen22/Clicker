#from distutils.version import Version, StrictVersion
from packaging.version import Version
from typing import NamedTuple

import requests

from config import RELEASES_URL


class UpdateException(Exception):
    pass


class Release(NamedTuple):
    version: Version
    changelog: str
    assets_url: str


def is_new_version_available(current_version: Version) -> bool:
    return current_version < get_last_release_from_repository(RELEASES_URL).version


def get_last_release_from_repository(repository_url: str) -> Release:
    response = requests.get(RELEASES_URL)
    if not response.ok:
        raise UpdateException
    releases: list[Release] = []
    for release_data in response.json():
        release = Release(
            version=Version(release_data["tag_name"]),
            changelog=release_data["body"],
            assets_url=release_data["assets_url"]
        )
        releases.append(release)
    releases.sort(key=lambda value: value.version)

    return releases[0]


if __name__ == "__main__":
    print(is_new_version_available(current_version=Version("v0.0.0")))
