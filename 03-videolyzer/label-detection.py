# coding: utf-8
import boto3
session = boto3.Session(profile_name='pythonProject')
s3 = session.resource('s3')
bucket = s3.create_bucket(Bucket='shawnvideolyzer95')
from pathlib import Path
get_ipython().run_line_magic('ls', '\\Users\\ShawnWong\\Downloads\\*mp4')
pathname = '~/Downloads/Pexels Videos 1711830.mp4'
path = Path(pathname).expanduser().resolve()
print(path)
print(type(path))
path.name
revisedPath = '/'.join(str(path).split('\\'))
print(revisedPath)
bucket.upload_file(str(path), str(path.name))
bucket.upload_file(str(revisedPath), str(path.name))
rekognition_client = session.client('rekognition')
response = rekognition_client.start_label_detection(Video={'S3Object': { 'Bucket': bucket.name, 'Name': path.name}})
response
job_id = response['JobId']
job_id
result = rekognition_client.get_label_detection(JobId=job_id)
result
result.keys()
result['JobStatus']
result['ResponseMetadata']
result['VideoMetadata']
result['Labels']
len(result['Labels'])
get_ipython().run_line_magic('history', '')
get_ipython().run_line_magic('save', 'label-detection.py 1-50')
