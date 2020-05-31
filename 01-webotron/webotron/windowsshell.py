#05.27.2020
@cli.command('sync')
@click.argument('pathname', type=click.Path(exists=True))
@click.argument('bucket')
def sync(pathname, bucket):
    "Sync contents of PATHNAME to BUCKET"
    s3_bucket = s3.Bucket(bucket)

    root = Path(pathname).expanduser().resolve()
    print("pathname is",pathname)
    print("root is ",root)
    def handle_directory(target):
        for p in target.iterdir():
            if p.is_dir(): handle_directory(p)
            if p.is_file():
                upload_file(s3_bucket, '/'.join(str(p).split('\\')), '/'.join(str(p.relative_to(root)).split('\\')))
                # print(root)
                # print(n)
                # print()
                # upload_file(s3_bucket, str(p), str(n))
                """
                print("p is ",p)
                print("str(p) is ",str(p))
                print("str(p).split('\\') is ",str(p).split('\\'))
                print("'/'.join(str(p).split('\\')) is ",'/'.join(str(p).split('\\')))
                整个上面的部分全部都是为了将windows的\变成/。
                """

    handle_directory(root)

    # root = Path(pathname).expanduser().resolve()
    #
    # def handle_directory(target):
    #     for p in target.iterdir():
    #         if p.is_dir(): handle_directory(p)
    #         if p.is_file(): print("Path: {}\n Key: {}".format(p,p.relative_to(root)))
    #
    # handle_directory(root)

PS C:\Users\ShawnWong\code\automating-aws-with-python\01-webotron> python webotron/webotron.py list-buckets
s3.Bucket(name='automatingawsshawn-newbucket')
s3.Bucket(name='automatingawswithpythonprojectbucket')
s3.Bucket(name='automatingawswithpythonprojectbucket2')
s3.Bucket(name='automatingawswithpythonprojectbucket3')
s3.Bucket(name='newnewnew9955shawnbucket')
PS C:\Users\ShawnWong\code\automating-aws-with-python\01-webotron> python webotron/webotron.py list-bucket-objects newnewnew9955shawnbucket
s3.ObjectSummary(bucket_name='newnewnew9955shawnbucket', key='css/main.css')
s3.ObjectSummary(bucket_name='newnewnew9955shawnbucket', key='images/Balinese-kitten1.jpg')
s3.ObjectSummary(bucket_name='newnewnew9955shawnbucket', key='images/Maine_coon_kitten_roarie.jpg')
s3.ObjectSummary(bucket_name='newnewnew9955shawnbucket', key='images/SFSPCA_Kitten.jpg')
s3.ObjectSummary(bucket_name='newnewnew9955shawnbucket', key='index.html')
PS C:\Users\ShawnWong\code\automating-aws-with-python\01-webotron> python webotron/webotron.py setup-bucket newnewnew9955shawnbucket
PS C:\Users\ShawnWong\code\automating-aws-with-python\01-webotron> python webotron/webotron.py setup-bucket newnewnew9955shawnbucket2
PS C:\Users\ShawnWong\code\automating-aws-with-python\01-webotron> python webotron/webotron.py --help
Usage: webotron.py [OPTIONS] COMMAND [ARGS]...

  Webotron deploys websites to AWS

Options:
  --help  Show this message and exit.

Commands:
  list-bucket-objects  List objects in an s3 bucket
  list-buckets         List all s3 buckets
  setup-bucket         Create and configure s3 bucket
  sync                 Sync contents of PATHNAME to BUCKET
PS C:\Users\ShawnWong\code\automating-aws-with-python\01-webotron> python webotron/webotron.py sync kitten_web/ newnewnew9955shawnbucket2
PS C:\Users\ShawnWong\code\automating-aws-with-python\01-webotron> python webotron/webotron.py sync kitten_web/ newnewnew9955shawnbucket2

import boto3
import click

from bucket import BucketManager

# session = boto3.Session(profile_name='pythonProject')
# bucket_manager = BucketManager(session)
# # s3 = session.resource('s3')
#
# @click.group()
# def cli():
#     "Webotron deploys websites to AWS"
#     pass
session = None
bucket_manager = None

@click.group()
@click.option('--profile', default=None,help="Use a given AWS profile.")

def cli(profile):
    """Webotron deploys websites to AWS."""
    global session, bucket_manager

    session_cfg = {}
    if profile:
        session_cfg['profile_name'] = profile
    session = boto3.Session(**session_cfg)
    bucket_manager = BucketManager(session)

@cli.command('list-buckets')
def list_buckets():
    """List all s3 buckets."""
    for bucket in bucket_manager.all_buckets():
        print(bucket)

@cli.command('list-bucket-objects')
@click.argument('bucket')
def list_bucket_objects(bucket):
    """List objects in an s3 bucket."""
    for obj in bucket_manager.all_objects(bucket):
        print(obj)

@cli.command('setup-bucket')
@click.argument('bucket')
def setup_bucket(bucket):
    """Create and configure S3 bucket."""
    s3_bucket = bucket_manager.init_bucket(bucket)
    bucket_manager.set_policy(s3_bucket)
    bucket_manager.configure_website(s3_bucket)
    return

@cli.command('sync')
@click.argument('pathname', type=click.Path(exists=True))
@click.argument('bucket')
def sync(pathname, bucket):
    """Sync contents of PATHNAME to BUCKET."""
    bucket_manager.sync(pathname, bucket)

if __name__ == '__main__':
    cli()
