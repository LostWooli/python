import boto3
import os
import time
import logging
from botocore.exceptions import ClientError

def upload_file(file_name, bucket, object_name):
    print("Attempting to upload "+file_name+"to "+bucket)
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
        print(response)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def process_event(helper, *args, **kwargs):
    ts = time.strftime("%Y/%m/%d/%H", time.gmtime(time.time()))
    
    helper.log_info("Alert action send_local_csv_to_s3 started.")
    report_keyword = helper.get_param("report_keyword")
    helper.log_info("report_keyword={}".format(report_keyword))
    s3_bucket_destination = helper.get_param("s3_bucket_destination")
    helper.log_info("s3_bucket_destination={}".format(s3_bucket_destination))
    files=os.listdir("/opt/splunk/var/run/splunk/csv")
    
    for file in files:
        #print(ts)
        if report_keyword in file:
            file_name="/opt/splunk/var/run/splunk/csv/"+file
            bucket=s3_bucket_destination
            object_name=ts+'/'+file
            upload_file(file_name, bucket, object_name)
        else:
            print("Nothing found")
    return 0

    #/year/month/day/hour/filename_timestamp.csv 