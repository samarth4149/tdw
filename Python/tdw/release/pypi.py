from typing import List
from subprocess import Popen, PIPE
import re
from pkg_resources import get_distribution


class PyPi:
    """
    Compare the version of the installed tdw Python module to the PyPi version.
    """

    @staticmethod
    def strip_post_release(v: str) -> str:
        """
        If the version number has a post-release suffix (a fourth number), strip it.

        :param v: The version number.

        :return: The version, stripped of the post-release suffix.
        """

        if len(v.split(".")) > 3:
            return '.'.join(v.split('.')[:3])
        else:
            return v

    @staticmethod
    def get_major_release(v: str) -> str:
        """
        :param v: The version number.

        :return: The major release number (example: in 1.7.0, the major release is 7).
        """

        return v.split(".")[1].strip()

    @staticmethod
    def _get_pypi_releases() -> List[str]:
        """
        :return: A list of all available PyPi releases.
        """

        # Get an error from  PyPi which will list all available versions.
        p = Popen(["pip3", "install", "tdw=="], stderr=PIPE, stdout=PIPE)
        p.wait()
        stdout, stderr = p.communicate()
        # From the list of available versions, get the last one (the most recent).
        versions = re.search(r"\(from versions: (.*)\)", stderr.decode("utf-8")).group(1).split(",")
        return [v.strip() for v in versions]

    @staticmethod
    def get_pypi_version(truncate: bool = False) -> str:
        """
        :param truncate: If true, remove the post-release number (the fourth number) if there is one.

        :return: The newest available tdw release on PyPi.
        """

        # From the list of available versions, get the last one (the most recent).
        v = PyPi._get_pypi_releases()[-1]

        # Strip the post-release suffix.
        if truncate:
            return PyPi.strip_post_release(v)
        else:
            return v

    @staticmethod
    def get_installed_tdw_version(truncate: bool = False) -> str:
        """
        :param truncate: If true, remove the post-release number (the fourth number) if there is one.

        :return: The version of the tdw Python module installed on this machine.
        """

        v = get_distribution("tdw").version

        # Strip the post-release suffix.
        if truncate:
            return PyPi.strip_post_release(v)
        else:
            return v

    @staticmethod
    def get_latest_post_release(v: str) -> str:
        """
        :param v: A three-part version string, e.g. 1.6.1

        :return: The most up-to-date version or post-release of the tdw module on PyPi with `v`, e.g. 1.6.1.10
        """

        releases = PyPi._get_pypi_releases()
        releases = sorted([r for r in releases if r.startswith(v)])
        if len(releases) == 0:
            return ""
        return releases[-1]

    @staticmethod
    def get_latest_minor_release(v: str) -> str:
        """
        :param v: The version number.

        :return: The most up-to-date version in this major release. (Example: if v == 1.5.0, this returns 1.5.5)
        """

        version = PyPi.strip_post_release(v)
        releases = PyPi._get_pypi_releases()
        releases = sorted([r for r in releases if r.startswith("1." + PyPi.get_major_release(version))])
        if len(releases) == 0:
            return ""
        return releases[-1]
