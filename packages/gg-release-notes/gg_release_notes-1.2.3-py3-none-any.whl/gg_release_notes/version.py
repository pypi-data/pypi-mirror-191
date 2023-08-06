from typing import Optional

from ghapi.all import GhApi

from gg_release_notes.config.github_config import GithubAPIConfig


class ReleaseVersion:
    """
    Class for getting and incrementing the version number of the current release in Github.
    """

    def __init__(self, github_configuration: GithubAPIConfig):
        self.github_configuration = github_configuration
        self.github_api: GhApi = github_configuration.github_api

    @property
    def _version_mapping(self) -> dict:
        """Maps the versioning type to the correct incrementation function."""
        return {
            "None": 2,
            "major": 0,
            "minor": 1,
            "patch": 2,
        }

    @property
    def current_version(self) -> str:
        """Gets the current version number of the release."""
        try:
            release_req = self.github_api.repos.get_latest_release()
            version = release_req.get("tag_name", "1.0.0")
        except:
            # No release exists yet
            version = "1.0.0"
        
        return str(version)

    def increment_version(
        self, current_version: str, versioning_type: Optional[str]
    ) -> str:
        """Increments the version number of the current release."""
        print(f"Current version: {current_version}")
        if self._version_mapping.get(versioning_type) == 2:
            version_list = current_version.split(".")
            version_list[self._version_mapping.get(str(versioning_type))] = str(
                int(version_list[self._version_mapping.get(str(versioning_type))]) + 1
            )
        else:
            version_list = current_version.split(".")
            version_list[self._version_mapping.get(str(versioning_type))] = str(
                int(version_list[self._version_mapping.get(str(versioning_type))]) + 1
            )

            # Reset all the other version numbers to 0
            for i in range(self._version_mapping.get(str(versioning_type)) + 1, 3):
                version_list[i] = "0"

        version = ".".join(version_list)
        print(f"New version: {version}")        
        return str(version)
