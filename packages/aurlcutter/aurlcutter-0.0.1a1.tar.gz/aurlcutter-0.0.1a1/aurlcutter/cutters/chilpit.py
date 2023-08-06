from .._base import BaseCutter
from .._validators import validate_url
from .._links import CHILPIT
from .._exceptions import CuttingErrorException

import logging

logger = logging.getLogger(__name__)


class Cutter(BaseCutter):
    """
    Chilp.it shortener implementation
    """

    api_url = CHILPIT

    async def cut(self, url: str) -> str:
        """
        Chilp.it request and get method

        Args:
            url (str): Url, that will be shortened

        Raises:
            CuttingErrorException: If we got invalid data from API

        Returns:
            str: Shortened url
        """
        url = await validate_url(url)
        response = await self._get(self.api_url, params={"url": url})

        if response.status_code == 200:
            return response.text.strip()

        raise CuttingErrorException(response.content)
