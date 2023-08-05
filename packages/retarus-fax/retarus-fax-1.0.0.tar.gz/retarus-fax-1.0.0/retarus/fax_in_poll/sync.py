import asyncio
from typing import List, Union

from .model import Client
from ._async import AsyncClient


class SyncClient(Client):
    def __init__(self, out_path: str, page_size: int, timeout: int, uris):
        self.client = AsyncClient(out_path, page_size, timeout, uris)
        self.loop = asyncio.new_event_loop()

    def fetch_fax_list(self, topic: str, ids: List[str] = None) -> List[dict]:
        res = self.loop.run_until_complete(self.client.fetch_fax_list(topic=topic, ids=ids))
        return res


    def download_fax(self, doc_url: str):
        res = self.loop.run_until_complete(self.client.download_fax(doc_url=doc_url))
        return res

    def acknowledge_fax(self, topic: str, ids: List[str]) -> Union[list, bool]:
        res = self.loop.run_until_complete(self.client.acknowledge_fax(topic=topic, ids=ids))
        return res