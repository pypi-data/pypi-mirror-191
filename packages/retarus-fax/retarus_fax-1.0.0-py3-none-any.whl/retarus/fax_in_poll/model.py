from typing import List
from abc import ABC, abstractmethod


class Client(object):
    """
    Offical retarus fax-in-poll SDK to use the fax in poll service provided by retarus inc.
    """

    def __init__(self, out_path: str, page_size: int = 10, timeout: int = 60):
        self.out_path = out_path
        self.page_size = page_size
        self.timeout = timeout

    def fetch_fax_list(self, topic: str) -> List[dict]:
        """
        Requests a list of faxes that are hold under the given topic.
        """
        pass

    def download_fax(self, doc_url: str):
        """
        Takes the given fax url and downloads it to the specified fax location [out_path].
        """
        pass
    def acknowledge_fax(self, ids: List[str]):
        """
        Akknowleges the list of fax ids, so they will be deleted from the retarus server and marked as completed.
        """
        pass
