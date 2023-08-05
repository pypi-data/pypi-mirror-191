from retarus.commons.config import Configuration
from retarus.fax.model import BulkRequest, Job, Client
from retarus.commons.transport import Transporter


class AsyncClient(Client):
    """
    Official Retarus Fax4App client SDK to send faxes with ease within your Python code.
    """
    def __init__(self, uris):
        self.transporter = Transporter(uris)

    async def send_fax_job(self, job: Job) -> str:
        data = job.exclude_optional_dict()
        path = f"/{Configuration.customer_number}/fax"
        res = await self.transporter.post(path, data)
        return res

    async def get_fax_report(self, job_id: str) -> dict:
        endpoint = f"{Configuration.customer_number}/fax/reports/{job_id}"
        res = await self.transporter.get(endpoint)
        return res

    async def get_fax_reports(self) -> list:

        path = f"{Configuration.customer_number}/fax/reports"
        res = await self.transporter.get(path)
        return res

    async def delete_fax_report(self, job_id: str):

        path = f"{Configuration.customer_number}/fax/reports/{job_id}"
        res = await self.transporter.delete(path)
        return res

    # async def bulk_operation(self, payload: BulkRequest):
    #     path = f"{Configuration.customer_number}/fax/reports"
    #     res = await self.transporter.post(path, payload.dict())
    #     return res

    async def delete_all_fax_reports(self) -> list:
        path = f"{Configuration.customer_number}/fax/reports"
        res = await self.transporter.delete(path)
        return res
