import os
import json
import sys
from retarus.commons.config import Configuration
from retarus.fax.client import FaxClient
from retarus.fax.model import Job, SendRecipient, Document


def _load_conf():
    with open("test_env.toml", "rb") as conf:
        if sys.version_info[1] >= 11:
            import tomllib
            return tomllib.load(conf)
        else: 
            import toml 
            return toml.load(conf) 


def set_env():
    config_data = _load_conf()
    for key, value in config_data.items():
        if type(value) == list:
            os.environ[key] = json.dumps(value)
            continue
        for k, v in value.items():
            os.environ[k] = str(v)


async def send_fax_for_fip_tests():
    Configuration.set_auth(os.environ["retarus_userid"], os.environ["retarus_fax_password"])
    Configuration.customer_number = os.environ["retarus_topic_user"]
    abc = FaxClient(True)
    doc = Document.from_path("tests/assets/test.pdf")
    recipients = SendRecipient(number=os.environ["retarus_fax_number"])
    job = Job(recipients=[recipients], documents=[doc])
    res = await abc.client.send_fax_job(job)
    print(res)