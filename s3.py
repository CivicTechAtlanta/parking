import boto
import boto.s3
import config

var = config.get_config()


def push_to_s3(filename, filecontents, aws_access_key_id, aws_secret_access_key, bucket):
    conn = boto.connect_s3(aws_access_key_id, aws_secret_access_key)
    
    bucket = conn.get_bucket(bucket)
    key = bucket.new_key(filename)
    
    key.set_contents_from_string(filecontents)


# If you run `python s3.py`, it will push the text `blah2` to your s3 bucket in the filename `test`
if __name__ == "__main__":
    AWS_ACCESS_KEY_ID = var["access_key"]
    AWS_SECRET_ACCESS_KEY = var["secret_access_key"]
    BUCKET = var["bucket"]
    push_to_s3("test", "blah2", AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, BUCKET)
