from __future__ import annotations
from pydantic import BaseModel, Field
from typing import List, Optional
import os
import base64
from enum import Enum

from retarus.commons.utils import to_camel_case

class RenderingOptions(BaseModel):
    paper_format: Optional[str] = Field()
    coverpage_template: str = Field()
    resolution: Optional[str] = Field()
    header: Optional[str] = Field()

    class Config:
       alias_generator = to_camel_case


class Document(BaseModel):
    name: str = Field()
    data: str = Field()
    charset: Optional[str] = Field()

    class Config:
        alias_generator = to_camel_case

    @staticmethod
    def from_path(file_name: str):
        with open(file_name, "rb") as file:
            res = file.read()
            encoded = base64.b64encode(res)
            object_name = os.path.basename(file_name)
            return Document(name=object_name, data=encoded)


class KeyValue(BaseModel):
    key: str = Field()
    value: str = Field()

    class Config:
        alias_generator = to_camel_case

    def __dict__(self):
        return {
            "key": self.key,
            "value": self.value
        }


class SendRecipient(BaseModel):
    number: str = Field()
    properties: Optional[List[KeyValue]] = None

    class Config:
        alias_generator = to_camel_case

    def __dict__(self):
        return {
            "number": self.number,
            "properties": self.properties
        }


class Job(BaseModel):
    """
    Create a Job instance to send it via fax.
    Minimum:
    recipients:list
    documents:list
    """
    recipients: List[SendRecipient] = Field()
    documents: List[Document] = Field()
    rendering_options: Optional[RenderingOptions] = Field()

    class Config:
        alias_generator = to_camel_case

    def exclude_optional_dict(model: BaseModel):
        return {**model.dict(exclude_unset=True), **model.dict(exclude_none=True)}


class Recipient(BaseModel):
    number: str = Field()
    properties: Optional[str] = Field()
    status: str = Field()
    reason: str = Field()
    send_ts: str = Field()
    duration_in_seconds: int = Field()
    send_to_number: str = Field()
    remote_cs_id: str = Field()

    class Config:
        alias_generator = to_camel_case


class Reference(BaseModel):
    costumer_defined_id: str = Field()
    billing_code: Optional[str] = Field()
    billing_ingo: Optional[str] = Field()

    class Config:
        alias_generator = to_camel_case


class FaxReport(BaseModel):
    job_id: str = Field() 
    recipient_status: Optional[List[Recipient]] = Field()
    pages: int = Field()
    reference: Reference = Field()
    
    class Config:
        alias_generator = to_camel_case


class Action(str, Enum):
    DELETE = "DELETE"
    GET = "GET"


class BulkRequest(BaseModel):
    """
    Specify the action typ of your request and your job ids.
    """
    action: str = None
    jobIds: List[str] = Field(default=None)

    class Config:
        use_enum_values = True
        alias_generator = to_camel_case

    def exclude_optional_dict(model: BaseModel):
        return {**model.dict(exclude_unset=True), **model.dict(exclude_none=True)}


class Client(object):
    """
    Official Retarus Fax4App client SDK to send faxes with ease within your Python code.
    """

    def send_fax_job(self, job: Job) -> str:
        """
        This method is used to prepare fax jobs to be transferred for processing. If a valid FaxJobRequest has been received by the Webservice, the Webservice sends a Job ID back that must be specified by the client when querying the job status.

        :param job:
        :return: job_id: str
        """

    def get_fax_report(self, job_id: str) -> dict:
        """
        Get the fax report created by the servers with the job_id returned by the [send_fax_job] function.
        :param job_id:
        :return: fax-report: dict
        """

    def get_fax_reports(self) -> list:
        """
        This URL returns a list of available status reports for completed fax jobs for the current account.

        Status reports are available for up to 30 days or until deleted.

        IMPORTANT: The results are limited to the oldes 1000 entries. It is recommended to delete the status reports after fetching them in order to retrieve the following ones.
        """

    def delete_fax_report(self, job_id: str):
        """
        Deletes the status report for a single job. Returns the Job ID

        :param job_id:
        :return:
        """

    # def bulk_operation(self, payload: BulkRequest):
    #     """
    #     Get or Delete fax report with a list set of job ids, specify in your request the action type: ["GET", "DELETE"] and your required job ids along.

    #     :param payload:
    #     :return:
    #     """

    def delete_all_fax_reports(self) -> list:
        """
        Deletes up to 1000 status reports for completed fax jobs for the current account, starting from the oldest ones. It returns the jobIds of deleted job reports.

        IMPORTANT: In case there are more than 1000 completed job reports, multiple calls of this method might be needed to delete them all.
        :return: list[dict]
        """
