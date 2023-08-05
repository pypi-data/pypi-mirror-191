import pytest
import os
import time
import asyncio 

from retarus.fax_in_poll.client import FaxInPollClient
from retarus.commons.config import Configuration
from setup import send_fax_for_fip_tests, set_env

# Unit test vaiables
#set_env()
Configuration.set_auth(os.environ["retarus_polling_user"], os.environ["retarus_polling_password"])
TOPIC = os.environ["topic"]
jobs = []

sdk = FaxInPollClient(True, timeout=0)
sync: FaxInPollClient = None


@pytest.mark.asyncio
async def test_create_instance_of_client():
    # Check if a client can be created
    client = FaxInPollClient(True)
    assert isinstance(client, FaxInPollClient)


def test_create_sync_client():
    global sync
    sync = FaxInPollClient(False, timeout=0)
    assert isinstance(sdk, FaxInPollClient)


def test_send_sync_request():
    global sync
    Configuration.set_auth(os.environ["retarus_topic_user"], os.environ["retarus_topic_password"])
    res = sync.client.fetch_fax_list(TOPIC)
    assert isinstance(res, list)


@pytest.mark.asyncio
async def test_list_fax_jobs():
    await send_fax_for_fip_tests()
    await asyncio.sleep(60)
    global sdk
    global jobs
    Configuration.set_auth(os.environ["retarus_topic_user"], os.environ["retarus_topic_password"])
    res = await sdk.client.fetch_fax_list(TOPIC)

    if isinstance(res, bool):
        assert res
    assert isinstance(res, list)
    assert not len(res) <= 0
    jobs= res


@pytest.mark.dependency("test_list_fax_jobs")
@pytest.mark.asyncio
async def test_download_fax():
    global sdk
    global jobs
    Configuration.set_auth(os.environ["retarus_topic_user"], os.environ["retarus_topic_password"])
    document_name: str = ""
    counter = -1
    for x in jobs:
        if len(x["documents"]) != 0:
            document_name = jobs[counter]["documents"][0]["url"].split("/")[-1]
            assert document_name.endswith(".pdf")
            counter -= 1
            break

    res = await sdk.client.download_fax(document_name)
    with open(document_name, "rb") as file:
        assert len(file.read()) != 0


@pytest.mark.dependency("test_download_fax")
@pytest.mark.asyncio
async def test_acknowledge_fax():
    global sdk
    global jobs
    Configuration.set_auth(os.environ["retarus_topic_user"], os.environ["retarus_topic_password"])
    
    ids = [x["id"] for x in jobs]
    await sdk.client.acknowledge_fax(TOPIC, ids)
    res = await sdk.client.fetch_fax_list(TOPIC)
    assert len(res) == 0