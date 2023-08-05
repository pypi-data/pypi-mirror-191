import os
from dotenv import load_dotenv 

from retarus.fax.model import Document, Job, SendRecipient
from retarus.commons.config import Configuration
from retarus.fax.client import FaxClient
from retarus.commons.region import Region

'''
How to use this example
1. Setup the SDK like described in the README file on top level of the repository. If 
   you need additonal help, please have a look at our OpenAPI here: 
   https://developers.retarus.com/docs/fax/api/sending-fax/
2. Create an .env file somewhere in your project. It must at least contain key / value
   pairs of "retarus_userid" and "retarus_fax_password" and may also contain 
   "retarus_customer_number" if you want to reference that too. You need the values to
   authenticate and optionally set the customer number as can be seen below. An entry 
   looks like this:
   retarus_userid=user123
   We recommend to create the .env file on the same level as this script.
3. This example will overtake the test PDF from the assets folder in the fax examples.
   Feel free to set any other path you like in the read_document function. Also, you
   should replace the recipient number in the main function by your own one to see a
   result when you send a fax.
4. When you are satisfied with your settings, execute this script. As a confirmation,
   this example prints the job ID that you can use to check it's status. Please see
   our example 'get_status_sync.py' for details on getting a status. Feel free to adjust
   the status handling in the way you like it. For example, you could report it in a
   logger and then save it to a log file.
'''


def initialize():
    # Here, you overtake credentials and customer number from the .env file and configure the SDK.
    Configuration.set_auth(os.environ["retarus_userid"], os.environ["retarus_fax_password"])
    Configuration.customer_number = os.environ["retarus_customer_number"]
    # You can choose from the regions Europe, America, Switzerland and Singapore
    Configuration.set_region(Region.Europe)

    # create a new recipient, read a file and return create a new document instance
    job = Job(recipients=[SendRecipient(number="+4900000000000")], documents=[Document.from_path("./assets/test.pdf")])
    return job


def send(job):
    # create a new client instance
    sdk = FaxClient(False)

    # send the fax to process via the client instance we just created
    res = sdk.client.send_fax_job(job)
    # prints the job_id returned by the server, if there was an error it will raise an exception
    print("Fax job was sent successfully, you can track it with job ID " + res['jobId'])
    return res



if __name__ == "__main__":
    # With load_dotenv, you load the env file needed in the initialize function.
    load_dotenv()
    job = initialize()
    res = send(job)
