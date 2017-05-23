import boto
import boto.s3
import sys
from boto.s3.key import Key
import config

vars = config.get_config()

AWS_ACCESS_KEY_ID = vars["access_key"]
AWS_SECRET_ACCESS_KEY = vars["secret_access_key"]
BUCKET = vars["bucket"]

def push_to_s3(filename, filecontents):
    conn = boto.connect_s3(AWS_ACCESS_KEY_ID,
            AWS_SECRET_ACCESS_KEY)
    
    bucket = conn.get_bucket('martaparking')
    key = bucket.new_key(filename)
    
    key.set_contents_from_string(filecontents)

if __name__ == "__main__":
    push_to_s3("test","blah2")
