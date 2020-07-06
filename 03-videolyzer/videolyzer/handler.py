import urllib
import os
import boto3
import json

def start_label_detection(bucket, key):
    rekognition_client = boto3.client('rekognition')
    response = rekognition_client.start_label_detection(
        Video={
            'S3Object': {
                'Bucket': bucket,
                'Name': key
            }
            },
        NotificationChannel={
            'SNSTopicArn': os.environ['REKOGNITION_SNS_TOPIC_ARN'],
            'RoleArn': os.environ['REKOGNITION_ROLE_ARN']
        })

    print(response)

    return

def get_video_labels(job_id):
    rekognition_client = boto3.client('rekognition')

    response = rekognition_client.get_label_detection(JobId=job_id)
    """
    We will only get back a maximum of 1000 labels at a time.
    so we need to check if reponse have next page
    """
    next_token = response.get('NextToken', None)

    while next_token:
        """
        while there's more data to get, we'll get the next page,
        we'll give it the job ID just like we did last time.
        And so we'll keep getting the next page until next token doesn't have a value.
        """
        next_page = rekognition_client.get_label_detection(
            JobId=job_id,
            NextToken=next_token
        )

        next_token = next_page.get('NextToken', None)
        """
        while loop get all the reponse results out and save to the response
        """
        response['Labels'].extend(next_page['Labels'])

    return response

def make_item(data):
    if isinstance(data, dict):
        return { k: make_item(v) for k, v in data.items() }
        #if data is dict, make_item for each value in the dictionary

    if isinstance(data, list):
        return [ make_item(v) for v in data ]
        #if data is list, make_item for each value in the list

    if isinstance(data, float):
        return str(data)
        #if data is float, make it a string

    return data

def put_labels_in_db(data, video_name, video_bucket):
    del data['ResponseMetadata']
    del data['JobStatus']

    data['videoName'] = video_name
    data['videoBucket'] = video_bucket

    dynamodb = boto3.resource('dynamodb')
    table_name = os.environ['DYNAMODB_TABLE_NAME']
    videos_table = dynamodb.Table(table_name)

    data = make_item(data)

    videos_table.put_item(Item=data)

    return

def start_processing_video(event, context):
    for record in event['Records']:
        start_label_detection(
            record['s3']['bucket']['name'],
            urllib.parse.unquote_plus(record['s3']['object']['key'])
        )

    return

def handle_label_detection(event, context):
    for record in event['Records']:
        message = json.loads(record['Sns']['Message'])
        job_id = message['JobId']
        s3_object = message['Video']['S3ObjectName']
        s3_bucket = message['Video']['S3Bucket']

    # print(event)
        response = get_video_labels(job_id)
        print(response)
        put_labels_in_db(response, s3_object, s3_bucket)
