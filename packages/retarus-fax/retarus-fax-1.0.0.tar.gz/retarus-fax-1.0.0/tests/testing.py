import os
import pytest

from retarus.fax.client import FaxClient
from retarus.fax.model import SendRecipient, Job, Document
from retarus.commons.config import Configuration

from setup import set_env


def init():
    Configuration.set_auth(os.environ["retarus_userid"], os.environ["retarus_fax_password"])
    Configuration.customer_number = os.environ["retarus_customer_number"]


#set_env()
init()

test_job_id = ""

sdk = FaxClient(False)


def test_send_fax_job():
    global test_job_id
    init()
    doc = Document.from_path("tests/assets/test.pdf")
    recipients = SendRecipient(number="4900000000000")
    job = Job(recipients=[recipients], documents=[doc])
    job_id = sdk.client.send_fax_job(job)
    print(job_id)
    test_job_id = job_id
    assert job_id != ""
    assert not isinstance(job_id, bool)


@pytest.mark.dependency("test_send_fax_job")
def test_get_fax_reports():
    global test_job_id
    print(test_job_id)
    res = sdk.client.get_fax_report(test_job_id["jobId"])
    print(res)
    assert res != {}
