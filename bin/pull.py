import boto3
import sys
import os
from urllib.parse import urlparse

def sync_from_s3(base_url):
    s3 = boto3.client('s3')

    parts = urlparse(base_url)
    bucket, prefix = (parts.netloc, parts.path[1:])


    keys = [f['Key'] for f in s3.list_objects_v2(Bucket=bucket, Prefix=prefix)['Contents']
              if f['Key'].endswith('.yml')  ]

    for key in keys:
        s3.download_file(bucket, key, os.path.join('data', os.path.basename(key)))

if __name__ == '__main__':
    base_url = "s3://gep-source-archive/models-august-2019"
    if len(sys.argv) > 1 and sys.argv[1]:
        base_url = sys.argv[1]
    sync_from_s3(base_url)
    



