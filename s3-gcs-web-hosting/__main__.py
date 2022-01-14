"""An Pulumi program to deploy Amazon S3 and Google Cloud Storage web hosting simultaneously"""

import pulumi, os, mimetypes
from pulumi_aws import s3
from pulumi_gcp import storage

web_content_dir = "www"

############
# Amazon S3
############

# Create an AWS resource (S3 Bucket)
s3_bucket = s3.Bucket(
    'pulumi-demo',
    website=s3.BucketWebsiteArgs(
        index_document="index.html",
    )
)

# Create contents file objects
for file in os.listdir(web_content_dir):
    filepath = os.path.join(web_content_dir, file)
    mime_type, _ = mimetypes.guess_type(filepath)
    obj = s3.BucketObject(
        file,
        acl='public-read',
        bucket=s3_bucket.id,
        content_type=mime_type,
        source=pulumi.FileAsset(filepath),
    )

# Export the URL
pulumi.export('s3_bucket_endpoint', pulumi.Output.concat('http://', s3_bucket.website_endpoint, "/index.html"))

######################
# Google Cloud Storage
######################

# Create a GCP resource (Storage Bucket)
gcs_bucket = storage.Bucket(
    'pulumi-demo',
    website=storage.BucketWebsiteArgs(
        main_page_suffix='index.html'
    ),
    uniform_bucket_level_access=True,
    )

# Create an IAM binding
bucket_iam_binding = storage.BucketIAMBinding(
    'pulumi-demo-iam-biding',
    bucket=gcs_bucket,
    role="roles/storage.objectViewer",
    members=["allUsers"],
)

# Create contents file objects
for file in os.listdir(web_content_dir):
    filepath = os.path.join(web_content_dir, file)
    mime_type, _ = mimetypes.guess_type(filepath)
    obj = storage.BucketObject(
        file,
        bucket=gcs_bucket,
        content_type=mime_type,
        name=file,
        source=pulumi.FileAsset(filepath),
    )

# Export the URL
pulumi.export('gcs_bucket_endpoint',  pulumi.Output.concat('http://storage.googleapis.com/', gcs_bucket.id, "/index.html"))
