# coding: utf-8
event = {'Records': [{'EventSource': 'aws:sns', 'EventVersion': '1.0', 'EventSubscriptionArn': 'arn:aws:sns:us-east-1:129736879650:handleLabelDetectionTopic:5205c14e-ce69-4206-bed0-f2772ddc4428', 'Sns': {'Type': 'Notification', 'MessageId': '1bf88923-06fc-52a8-93ee-de5bb8af300a', 'TopicArn': 'arn:aws:sns:us-east-1:129736879650:handleLabelDetectionTopic', 'Subject': None, 'Message': '{"JobId":"34040f820c717342c25e38bbf7fd8bab6ae684bd1516e9b1975f64139eab83ab","Status":"SUCCEEDED","API":"StartLabelDetection","Timestamp":1593752595695,"Video":{"S3ObjectName":"videopexel123.mp4","S3Bucket":"shawnwongvideolyzer95"}}', 'Timestamp': '2020-07-03T05:03:15.797Z', 'SignatureVersion': '1', 'Signature': 'ofk7f6eHNvs3nCKNEYDpZ5u+sh3D11Qrlw1RaOf6LwRtbcfjsAboKeOrMWva/lEX0in6tSjMUgY8xQo2xwW2YD04KdpK/6qs8N5DPRgya5UU8saW1gEOfqcb87aR08KNDRF8F0NVtvhBVoUgCkO7cRNnySMlHS3S+x3mUwaR42c2m/qTp8tdQCgy7fWKG8dOr8Fkso0eARmzPTIRIUeqahqLheAQ8vUvYgGNLRAtVvKWdxbYPnkxYeHPLmupZW/BRd9RK/sECTzugeMyjYoPf6Hd7oDKIQ/mmEuvyR8ZAiUF+xbngibmuVivsOYIRj3TrZDLQ2zAV1mPiwwB07G5wA==', 'SigningCertUrl': 'https://sns.us-east-1.amazonaws.com/SimpleNotificationService-a86cb10b4e1f29c941702d737128f7b6.pem', 'UnsubscribeUrl': 'https://sns.us-east-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-1:129736879650:handleLabelDetectionTopic:5205c14e-ce69-4206-bed0-f2772ddc4428', 'MessageAttributes': {}}}]}
event.keys()
event['Records'][0].keys()
event['Records'][0]['EventVersion']
event['Records'][0]['EventSource']
event['Records'][0]['EventSubscriptionArn']
event['Records'][0]['Sns']
event['Records'][0]['Sns']['Message']
import json
json.loads(event['Records'][0]['Sns']['Message'])
get_ipython().run_line_magic('save', 'handle-sns-event-example.py 1-33')

"""
This is how Records looks like after we decompose it
{'Records':
    [
        {
        'EventSource': 'aws:sns',
        'EventVersion': '1.0',
        'EventSubscriptionArn': 'arn:aws:sns:us-east-1:129736879650:handleLabelDetectionTopic:5205c14e-ce69-4206-bed0-f2772ddc4428',
        'Sns':
            {
            'Type': 'Notification',
            'MessageId': '1bf88923-06fc-52a8-93ee-de5bb8af300a',
            'TopicArn': 'arn:aws:sns:us-east-1:129736879650:handleLabelDetectionTopic',
            'Subject': None,
            'Message':
                '{
                "JobId":"34040f820c717342c25e38bbf7fd8bab6ae684bd1516e9b1975f64139eab83ab",
                "Status":"SUCCEEDED",
                "API":"StartLabelDetection",
                "Timestamp":1593752595695,
                "Video":
                    {
                    "S3ObjectName":"videopexel123.mp4",
                    "S3Bucket":"shawnwongvideolyzer95"
                    }
                }',
            'Timestamp': '2020-07-03T05:03:15.797Z',
            'SignatureVersion': '1',
            'Signature': 'ofk7f6eHNvs3nCKNEYDpZ5u+sh3D11Qrlw1RaOf6LwRtbcfjsAboKeOrMWva/lEX0in6tSjMUgY8xQo2xwW2YD04KdpK/6qs8N5DPRgya5UU8saW1gEOfqcb87aR08KNDRF8F0NVtvhBVoUgCkO7cRNnySMlHS3S+x3mUwaR42c2m/qTp8tdQCgy7fWKG8dOr8Fkso0eARmzPTIRIUeqahqLheAQ8vUvYgGNLRAtVvKWdxbYPnkxYeHPLmupZW/BRd9RK/sECTzugeMyjYoPf6Hd7oDKIQ/mmEuvyR8ZAiUF+xbngibmuVivsOYIRj3TrZDLQ2zAV1mPiwwB07G5wA==',
            'SigningCertUrl': 'https://sns.us-east-1.amazonaws.com/SimpleNotificationService-a86cb10b4e1f29c941702d737128f7b6.pem',
            'UnsubscribeUrl': 'https://sns.us-east-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-1:129736879650:handleLabelDetectionTopic:5205c14e-ce69-4206-bed0-f2772ddc4428',
            'MessageAttributes': {}
            }
        }
    ]
}
"""
