from typing import List

from retarus.commons.region import Region, RegionUri

from ._async import AsyncClient
from .sync import SyncClient
from .model import Client


class FaxInPollClient(object):
    """
    Official Retarus Fax In Poll Client to poll the received fax from the retarus server.
    """
    __fax_in_poll_uris: List[RegionUri] = [
        RegionUri(
            region=Region.Europe,
            ha_uri="https://api.us2.retarus.com/faxin",
            urls=["https://api.us2.retarus.com/faxin"]
        )
    ]

    def __init__(self, is_async: bool = False, download_path: str = "", page_size: int = 10, timeout: int = 60):
        self.is_async = is_async
        if self.is_async:
            self.client: Client = AsyncClient(download_path, page_size, timeout, self.__fax_in_poll_uris)
        else:
            self.client: Client = SyncClient(download_path, page_size, timeout, self.__fax_in_poll_uris)