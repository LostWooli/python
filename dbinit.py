import pymysql
import boto3
import json

def sm_aws_credentials():

    secret_name = f"/dbcreds/application_cbapi"
    client = boto3.client('secretsmanager', region_name='us-east-1')
    get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    payload = get_secret_value_response.get('SecretString').encode('utf8')
    parsed = json.loads(payload)
    password = str(parsed.get('main-dev.rds.chargebacks911.com'))
    host = "main-dev.rds.chargebacks911.com"
    username = "application_cbapi"
    return password, host, username

def init_db(conn):
    with conn.cursor() as cur:
        print("executng")
        cur.execute("SELECT VERSION()")
        version = cur.fetchone()
        cur.execute('SELECT NOW();')
        result = cur.fetchone()
        conn.commit()
        print(result)

def initialize_database():
    password, host, username = sm_aws_credentials()
    conn = pymysql.connect(host=host, user=username, passwd=password, connect_timeout=5)
    print("trying to connect to rds_host")
    init_db(conn)


def lambda_handler(event, context):
    initialize_database()