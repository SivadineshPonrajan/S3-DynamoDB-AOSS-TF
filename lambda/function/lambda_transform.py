import os
import io
import re
import uuid
import json
import boto3
import pandas as pd
from opensearchpy import OpenSearch, helpers


# Configure S3 and DynamoDB
s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

# OpenSearch Connection String
def get_connection_string():
    aoss_username = os.environ['OPENSEARCH_USERNAME']
    aoss_password = os.environ['OPENSEARCH_PASSWORD']
    aoss_endpoint = os.environ['OPENSEARCH_ENDPOINT']
    connection_string = "https://{}:{}@{}:443".format(aoss_username, aoss_password, aoss_endpoint)
    return connection_string

connection_string = get_connection_string()
opensearch_client = OpenSearch([connection_string])

def lambda_handler(event, context):
    # Get the S3 bucket data
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    # Read the CSV file from S3
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
    except Exception as e:
        print(e)
        raise e
    
    csv_content = response['Body'].read().decode('utf-8')
    df = pd.read_csv(io.StringIO(csv_content))

    if df.empty:
        return {
            'statusCode': 200,
            'body': json.dumps('No valid data found in the CSV file')
        }
    
    df = df.dropna()  # Remove rows with missing values
    df['Comment'] = df['Comment'].str.strip()  # Remove whitespaces front and back
    
    # Get email using regex
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    df['Email'] = df.apply(lambda row: pd.Series(re.findall(email_pattern, row['Comment'])).iloc[0] 
                           if pd.Series(re.findall(email_pattern, row['Comment'])).any() 
                           else row['Email'], axis=1)
    
    # Generate unique user_id
    df['user_id'] = df.apply(lambda row: str(uuid.uuid4()), axis=1)

    successful_items = []
    failed_items = []

    # Load data into DynamoDB
    with table.batch_writer() as batch:
        for _, row in df.iterrows():
            item = row.to_dict()
            try:
                batch.put_item(Item=item)
                successful_items.append(item)
            except Exception as e:
                print(f"Error loading item {item} into DynamoDB: {e}")
                failed_items.append(item)

    print(f"Successfully inserted {len(successful_items)} items into DynamoDB")
    print(f"Failed to insert {len(failed_items)} items into DynamoDB")

    # Bulk insert into OpenSearch and insert only successful items
    if successful_items:
        try:
            actions = [
                {
                    "_index": "customer_comment",
                    "_id": item['user_id'],
                    "_source": item
                }
                for item in successful_items
            ]
            response = helpers.bulk(opensearch_client, actions)
            print(f"Bulk indexing response: {response}")
        except Exception as e:
            print(f"Error bulk indexing items in OpenSearch: {e}")
    else:
        print("No items to index in OpenSearch as all DynamoDB insertions failed")