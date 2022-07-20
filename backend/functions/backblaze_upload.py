import os
from dotenv import load_dotenv

from b2sdk.v2 import *

load_dotenv('../.env')

def b2_upload(file, folder):
    B2_BUCKET = os.environ.get("B2_BUCKET")
    B2_KEY_ID = os.environ.get("B2_KEY_ID")
    B2_KEY = os.environ.get("B2_KEY")

    b2_destination = f'{folder}/{file}'

    info = InMemoryAccountInfo()
    b2_api = B2Api(info)
    b2_api.authorize_account("production", B2_KEY_ID, B2_KEY)
    bucket = b2_api.get_bucket_by_name(B2_BUCKET)
    print('Uploading to BackBlaze')
    result = bucket.upload_local_file(
            local_file=file,
            file_name=b2_destination
        )
    print('Successfully uploaded to BackBlaze')
    return(result)