import os

import requests

def post_to_slack(event, context):
    slack_webhook_url = os.environ['SLACK_WEBHOOK_URL']

    slack_message = "From {source} at {detail[StartTime]}: {detail[Description]}".format(**event)
    data = { "text": slack_message }
    requests.post(slack_webhook_url, json=data)

    return

# import json
#
#
# def hello(event, context):
#     print(event)
#
#     return {
#         "message": "Go Serverless v1.0! Your function executed successfully!",
#         "event": event
#     }
# import os
#
# def post_to_slack(event, context):
#     slack_webhook_url = os.environ['SLACK_WEBHOOK_URL']
#     print(slack_webhook_url)
#     print(event)
#
#     return
