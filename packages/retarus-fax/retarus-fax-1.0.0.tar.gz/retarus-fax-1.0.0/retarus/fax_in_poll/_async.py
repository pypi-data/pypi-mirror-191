from typing import List, Union
import logging
from retarus.commons.config import Configuration
from .model import Client
from retarus.commons.region import RegionUri
from retarus.commons.exceptions import RetarusSDKError
from retarus.commons.transport import Transporter

class RetarusRessourceNotFound(RetarusSDKError):
    pass

class AsyncClient(Client):

    def __init__(self, out_path: str, page_size: int, timeout: int, url: List[RegionUri]):
        # checks if the specified [out_pat] ends with a slash so the name of the to save file can be appended
        if not out_path.endswith("/") and len(out_path) != 0:
            out_path =+ "/"
        self.out_path = out_path
        self.page_size = page_size
        self.timeout = timeout
        self.transporter = Transporter(url)


    async def fetch_fax_list(self, topic: str, ids: List[str] = None):
        data = []
        path = f"/topics/{topic}"
        if not ids is None:
            ids = "%".join(ids)
        query_params = {"fetch": self.page_size, "timeout": self.timeout, "ids": ids}
        res = await self.transporter.post(path, {}, remove_none(query_params))
        if "results" in res:
            data = res["results"]
        return data
        

    async def download_fax(self, doc_url: str):
        filename = doc_url.split("/")[-1]
        uri = f"files/{filename}"
        res = await self.transporter.get(uri)
        with open(f"{self.out_path}{filename}", "wb") as file:
            file.write(res)
            if file == False:
                raise RetarusRessourceNotFound()


    async def acknowledge_fax(self, topic: str, ids: List[str]) -> Union[list, bool]:
        path = f"/topics/{topic}"
        if not ids is None:
            ids:str = ",".join(ids)
            ids.encode("utf8")
        query_params = {"fetch": 0, "timeout": self.timeout, "ids": ids, "toString": ""}
        res = await self.transporter.post(path, {}, remove_none(query_params))
        if "results" in res:
            return []
        return res


def remove_none(data: dict) -> dict:
    xy = {}
    for x, y in data.items():
        if y == None:
            continue
        xy[x] = y
    return xy