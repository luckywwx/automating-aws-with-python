# coding: utf-8
import boto3
session = boto3.Session(profile_name='pythonProject')
as_client = session.client('autoscaling')
as_client.describe_auto_scaling_groups()
as_client.describe_policies()
as_client.execute_policy(AutoScalingGroupName='Notifon Example Group',PolicyName='Scale Down')
as_client.execute_policy(AutoScalingGroupName='Notifon Example Group',PolicyName='Scale Up')
