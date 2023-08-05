from typing import List

from .sync import SyncFaxClient
from .model import Client
from ._async import AsyncClient
from retarus.commons.region import Region, RegionUri


class FaxClient(object):
    """
    Official Retarus Fax4App client SDK to send faxes with ease within your Python code.
    """

    __fax_uris: List[RegionUri] = [
        RegionUri(
            region=Region.Europe,
            ha_uri="https://faxws-ha.de.retarus.com",
            urls=["https://faxws.de2.retarus.com", "https://faxws.de1.retarus.com"],
        ),
        RegionUri(
            region=Region.America,
            ha_uri="https://faxws-ha.us.retarus.com",
            urls=["https://faxws.us2.retarus.com", "https://faxws.us1.retarus.com"],
        ),
        RegionUri(
            region=Region.Switzerland,
            ha_uri="https://faxws-ha.ch.retarus.com",
            urls=["https://faxws.ch1.retarus.com"],
        ),
        RegionUri(
            region=Region.Singapore,
            ha_uri="https://faxws.sg1.retarus.com",
            urls=["https://faxws.sg1.retarus.com"],
        ),
    ]

    def __init__(self, is_async: bool = False):
        self.is_async = is_async
        if is_async:
            self.client: Client = AsyncClient(self.__fax_uris)
        else:
            self.client: Client = SyncFaxClient(self.__fax_uris)
