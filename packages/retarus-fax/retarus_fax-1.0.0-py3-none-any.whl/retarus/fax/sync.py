import asyncio

from ._async import AsyncClient
from .model import BulkRequest, Job, Client


class SyncFaxClient(Client):
    """
    Official Retarus Fax4App client SDK to send faxes with ease within your Python code.
    """

    def __init__(self, uris):
        self.client = AsyncClient(uris)
        self.loop = asyncio.new_event_loop()

    def send_fax_job(self, job: Job):
        res = self.loop.run_until_complete(self.client.send_fax_job(job))
        return res

    def get_fax_report(self, job_id):
        res = self.loop.run_until_complete(self.client.get_fax_report(job_id))
        return res

    def get_fax_reports(self):
        res = self.loop.run_until_complete(self.client.get_fax_reports())
        return res

    def delete_fax_report(self, job_id: str):
        res = self.loop.run_until_complete(self.client.delete_fax_report(job_id))
        return res

    # def bulk_operation(self, payload: BulkRequest):
    #     res = self.loop.run_until_complete(self.client.bulk_operation(payload))
    #     return res

    def delete_all_fax_reports(self):
        res = self.loop.run_until_complete(self.client.delete_all_fax_reports())
        return res