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
import os

def post_to_slack(event, context):
    slack_webhook_url = os.environ['SLACK_WEBHOOK_URL']
    print(slack_webhook_url)
    print(event)

    return
