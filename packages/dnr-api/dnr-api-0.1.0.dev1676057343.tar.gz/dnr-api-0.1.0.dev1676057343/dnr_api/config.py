import os
from dataclasses import dataclass
from distutils.util import strtobool


@dataclass
class Config:
    """Config for dnr-api."""

    base_url: str = "https://nednr.nebraska.gov/IwipApi"

    @classmethod
    def make_url(cls, route: str) -> str:
        """Create a full URL from the endpoint route."""
        return os.path.join(cls.base_url, route.lstrip("/"))

    @classmethod
    def dnr_token(self) -> str:
        dnr_token = os.getenv("DNR_TOKEN")
        if dnr_token is None:
            raise ValueError("Please set the DNR_TOKEN environment variable")
        return dnr_token

    @classmethod
    def api_test(self) -> bool:
        api_test = os.getenv("API_TEST", "false")
        return strtobool(api_test)
