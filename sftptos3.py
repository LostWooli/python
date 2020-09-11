import os
import boto3
def list_of_files(path):
    full_file_path = []
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            full_file_path.append(os.path.join(root, name))
            #file_path = os.path.join(root, name).split('/')[-1]
    return full_file_path
def do_something_with_files(file_list):
    for item in file_list:
        if os.path.isfile(item):
            print(item)
            sync_to_s3(item)

def sync_to_s3(item, bucket_name="492239587024sftptest"):
    s3 = boto3.resource('s3')
    s3.Object(bucket_name, item).put(item)

do_something_with_files(list_of_files('/Users/jtaschetti/Documents/test'))


