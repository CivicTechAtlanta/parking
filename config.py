publish_to_s3 = False
access_key = ""
secret_access_key = ""
bucket = ""


def get_config():
    return {"publish_to_s3": publish_to_s3, "access_key": access_key,"secret_access_key": secret_access_key,
            "bucket": bucket}

