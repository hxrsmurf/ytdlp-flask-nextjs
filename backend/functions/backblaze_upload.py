import os
import sys
import time

from dotenv import load_dotenv

from b2sdk.v2 import *

load_dotenv('.env')

B2_BUCKET = os.environ.get("B2_BUCKET")
B2_KEY_ID = os.environ.get("B2_KEY_ID")
B2_KEY = os.environ.get("B2_KEY")

info = InMemoryAccountInfo()
b2_api = B2Api(info)
b2_api.authorize_account("production", B2_KEY_ID, B2_KEY)
bucket = b2_api.get_bucket_by_name(B2_BUCKET)

def b2_upload(file, video_id):
    b2_destination = f'videos/{video_id}/{file}'
    print('Uploading to BackBlaze')
    result = bucket.upload_local_file(
            local_file=file,
            file_name=b2_destination
        )
    print('Successfully uploaded to BackBlaze')
    return(result)

def b2_sync(video_id):
    # https://b2-sdk-python.readthedocs.io/en/master/api/sync.html
    source_folder = parse_sync_folder(f'{video_id}', b2_api)
    destination_folder = parse_sync_folder(f'b2://{B2_BUCKET}/videos/{video_id}', b2_api)

    synchronizer = Synchronizer( max_workers=100, dry_run=False )
    no_progress = False
    try:
        with SyncReport(sys.stdout, no_progress) as reporter:
            synchronizer.sync_folders(
                source_folder=source_folder,
                dest_folder=destination_folder,
                now_millis=int(round(time.time() * 1000)),
                reporter=reporter
            )
        return('Success')
    except Exception as e:
        print(e)
        return('Failure')