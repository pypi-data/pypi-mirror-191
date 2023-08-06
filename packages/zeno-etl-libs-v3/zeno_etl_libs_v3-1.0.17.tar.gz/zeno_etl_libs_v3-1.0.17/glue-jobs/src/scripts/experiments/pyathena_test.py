import boto3
import pandas as pd

s3 = boto3.resource('s3')
s3_client = boto3.client('s3')
athena_client = boto3.client(service_name='athena', region_name='ap-south-1')
bucket_name = 'aws-glue-temporary-921939243643-ap-south-1'
print('Working bucket: {}'.format(bucket_name))

def run_query(client, query):
    response = client.start_query_execution(
        QueryString=query,
        QueryExecutionContext={'Database': 'development'},
        ResultConfiguration={'OutputLocation': 's3://{}/athena/'.format(bucket_name)},
    )
    return response

def validate_query(client, query_id):
    resp = ["FAILED", "SUCCEEDED", "CANCELLED"]
    response = client.get_query_execution(QueryExecutionId=query_id)
    # wait until query finishes
    while response["QueryExecution"]["Status"]["State"] not in resp:
        response = client.get_query_execution(QueryExecutionId=query_id)

    return response["QueryExecution"]["Status"]["State"]

def read(query):
    print('start query: {}\n'.format(query))
    qe = run_query(athena_client, query)
    qstate = validate_query(athena_client, qe["QueryExecutionId"])
    print('query state: {}\n'.format(qstate))

    file_name = "athena/{}.csv".format(qe["QueryExecutionId"])
    obj = s3_client.get_object(Bucket=bucket_name, Key=file_name)
    return pd.read_csv(obj['Body'])

time_entries_df = read('select * from waba_campaigns_cohort limit 10')
print(time_entries_df)