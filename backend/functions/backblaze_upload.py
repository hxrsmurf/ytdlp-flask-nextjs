import os
from dotenv import load_dotenv

from b2sdk.v2 import *

load_dotenv('../.env')

def b2_upload(file):
    B2_BUCKET = os.environ.get("B2_BUCKET")
    B2_KEY_ID = os.environ.get("B2_KEY_ID")
    B2_KEY = os.environ.get("B2_KEY")

    file = '../' + file.replace('\\','/')
    b2_destination = file.split('../static/')[1]

    info = InMemoryAccountInfo()
    b2_api = B2Api(info)
    b2_api.authorize_account("production", B2_KEY_ID, B2_KEY)
    bucket = b2_api.get_bucket_by_name(B2_BUCKET)
    print('Uploading to BackBlaze')
    bucket.upload_local_file(
            local_file=file,
            file_name=b2_destination
        )