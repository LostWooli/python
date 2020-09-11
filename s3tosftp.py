import boto3
import pysftp as sftp
import json
import os

s3 = boto3.resource('s3')

def getusersecret():
    secret_name = f"ssftp.artefactsys.com"
    client = boto3.client('secretsmanager')
    get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    payload = get_secret_value_response.get('SecretString').encode('utf8')
    parsed = json.loads(payload)
    for key,values in parsed.items():
        sftpname = key
        sftppassword = values
    push_file_to_server(sftpname, sftppassword)

#Download S3 file
def download_file(folder, object_key):
    s3.Object('ers3-sftp-prd-us', folder+"/"+object_key).download_file(object_key)

#Send to SFTP
def push_file_to_server(sftpname, sftppassword):
    cnopts = sftp.CnOpts()
    cnopts.hostkeys = None
    s = sftp.Connection(host='ssftp.artefactsys.com', username=sftpname, password=sftppassword, cnopts=cnopts)
    local_path = object_key
    remote_path = "cb911/"+object_key

    s.put(local_path, remote_path)
    s.close()

#def lambda_handler(event, context):
#    for record in event['Records']:
#        print(record)

folder = "firstdata"
object_key = "CL9DFMDE.20483.NAGW-BWCKX001.234960031990.d.20171128.dfm.20200301"
download_file(folder, object_key)
getusersecret()

#Cleanup
if os.path.exists(object_key):
  os.remove(object_key)
