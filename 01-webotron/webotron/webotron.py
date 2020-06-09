import boto3
import click

from webotron.bucket import BucketManager
from webotron.domain import DomainManager
from webotron.certificate import CertificateManager
from webotron.cdn import DistributionManager
from webotron import util
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
domain_manager = None
cert_manager = None
dist_manager = None

@click.group()
@click.option('--profile', default=None,help="Use a given AWS profile.")

def cli(profile):
    """Webotron deploys websites to AWS."""
    global session, bucket_manager, domain_manager, cert_manager, dist_manager

    session_cfg = {}
    if profile:
        session_cfg['profile_name'] = profile
    session = boto3.Session(**session_cfg)
    bucket_manager = BucketManager(session)
    domain_manager = DomainManager(session)
    cert_manager = CertificateManager(session)
    dist_manager = DistributionManager(session)

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
    print(bucket_manager.get_bucket_url(bucket_manager.s3.Bucket(bucket)))

@cli.command('setup-domain')
@click.argument('domain')
def setup_domain(domain):
    """Configure DOMAIN to point to BUCKET."""
    #Get a bucket by name.
    bucket = bucket_manager.get_bucket(domain)

    zone = domain_manager.find_hosted_zone(domain) or domain_manager.create_hosted_zone(domain)

    endpoint = util.get_endpoint(bucket_manager.get_region_name(bucket))
    domain_manager.create_s3_domain_record(zone, domain, endpoint)
    print("Domain configured: http://{}".format(domain))

@cli.command('find-cert')
@click.argument('domain')
def find_cert(domain):
    """Find a certificate for <DOMAIN>."""
    print(cert_manager.find_matching_cert(domain))


@cli.command('setup-cdn')
@click.argument('domain')
@click.argument('bucket')
def setup_cdn(domain, bucket):
    """Set up CloudFront CDN for DOMAIN pointing to BUCKET."""
    """根据domain name得到对应cloudFront的distribution"""
    dist = dist_manager.find_matching_dist(domain)
    #如果找不到这个distribution，就创一个。
    if not dist:
        cert = cert_manager.find_matching_cert(domain)
        if not cert:  # SSL is not optional at this time
            print("Error: No matching cert found.")
            return

        dist = dist_manager.create_dist(domain, cert)
        #CloudFront的创建需要时间。
        print("Waiting for distribution deployment...")
        dist_manager.await_deploy(dist)

    """找到domain name对应的zone"""
    zone = domain_manager.find_hosted_zone(domain) or domain_manager.create_hosted_zone(domain)

    """在domain name的host zone里创造一个cloudFront record"""
    domain_manager.create_cf_domain_record(zone, domain, dist['DomainName'])
    print("Domain configured: https://{}".format(domain))

    return

if __name__ == '__main__':
    cli()
