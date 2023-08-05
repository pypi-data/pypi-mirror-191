import logging
import os
import json
import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from retarus.fax.client import FaxClient
from retarus.commons.config import Configuration
from retarus.fax.model import FaxReport, Job, Document, SendRecipient


fax_out_path = "out/"

# env variables
user_id = os.environ["retarus_userid"]
password = os.environ["retarus_password"]
customer_number = os.environ["customer_number"]

# Configure the SDK
Configuration.set_auth(user_id, password)
Configuration.customer_number = customer_number

client = FaxClient(is_async=False)


# utility function
def write_report(report: FaxReport, job_id: str):
    with open(f"in/{job_id}.json") as file:
        json.dump(report, file)


def detect(filename: str):
    """
    The pdf must be named after following scheme:
    'faxNumber_csid.pdf'
    """
    name = filename.split('/')[-1]
    if filename.endswith(".pdf") and "_" in filename:
        res = name.split("_")
        fax_number = res[0]
        print(fax_number)
        if fax_number.isdecimal():
            cs_id = res[1]
            # prepare fax job
            doc = Document.from_path(filename)
            recipient = SendRecipient(number=fax_number)
            job = Job(recipients=[recipient], documents=[doc])

            # send fax
            res = client.client.send_fax_job(job)
            is_processed = False

            # runs as long as the fax state is PENDING
            while is_processed == False:
                report = client.client.get_fax_report(res)
                print(report)
                if report["recipientStatus"][0]["status"] != "PENDING":
                    write_report(report, res)
                    is_processed = True
                time.sleep(40)

            return None
    logging.error(f"Could not send fax({filename}), file does not fulfill the filename schema.")


class ActionEventHandler(FileSystemEventHandler):
    def __init__(self, logger=None):
        super().__init__()

    def on_moved(self, event):
        super().on_moved(event)

    def on_created(self, event):
        super().on_created(event)

        if not event.is_directory:
            detect(event.src_path)


format = "%(asctime)s | %(lineno)d | %(levelname)s | %(funcName)s | %(message)s"
logging.basicConfig(level=logging.INFO, format=format)
event_handler = ActionEventHandler()
observer = Observer()
observer.schedule(event_handler, path=fax_out_path, recursive=True)
observer.start()

try:
    while True:
        time.sleep(1)
finally:
    observer.stop()
    observer.join()
