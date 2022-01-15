# Host Static Website on Amazon S3 and Google Cloud Storage simultaneously

This sample shows how to deploy statice website on Amazon S3 and Google Cloud Storage simultaineously by using [Pulumi](https://www.pulumi.com/)

## Deploying and running the program

1. Create a new stack:

    ```bash
    $ pulumi stack init s3-gcs-web-hosting
    ```

1. Set the AWS region:

    ```bash
    $ pulumi config set aws:region us-west-2
    ```

1. Set the GCP project and region

    ```bash
    $ pulumi config set gcp:project [your-gcp-project]
    $ pulumi config set gcp:region us-west2
    ```

1. Run `pulumi up` to preview and deploy changes.  After the preview is shown you will be
    prompted if you want to continue or not.

    ```bash
    $ pulumi up
    Previewing update (s3-gcs-web-hosting)

    View Live: https://app.pulumi.com/xxxxxxxx/s3-gcs-web-hosting/s3-gcs-web-hosting/previews/xxxxxxxxxxxxxxxxxx

        Type                             Name                                   Plan       
    +   pulumi:pulumi:Stack              s3-gcs-web-hosting-s3-gcs-web-hosting  create     
    +   ├─ aws:s3:Bucket                 pulumi-demo                            create     
    +   ├─ gcp:storage:Bucket            pulumi-demo                            create     
    +   ├─ aws:s3:BucketObject           index.html                             create     
    +   ├─ aws:s3:BucketObject           style.css                              create     
    +   ├─ aws:s3:BucketObject           image.jpg                              create     
    +   ├─ gcp:storage:BucketObject      index.html                             create     
    +   ├─ gcp:storage:BucketObject      style.css                              create     
    +   ├─ gcp:storage:BucketObject      image.jpg                              create     
    +   └─ gcp:storage:BucketIAMBinding  pulumi-demo-iam-biding                 create     
    
    Resources:
        + 10 to create

    Do you want to perform this update? yes
    Updating (s3-gcs-web-hosting)

    View Live: https://app.pulumi.com/xxxxxx/s3-gcs-web-hosting/s3-gcs-web-hosting/updates/1

        Type                             Name                                   Status      
    +   pulumi:pulumi:Stack              s3-gcs-web-hosting-s3-gcs-web-hosting  created     
    +   ├─ aws:s3:Bucket                 pulumi-demo                            created     
    +   ├─ gcp:storage:Bucket            pulumi-demo                            created     
    +   ├─ gcp:storage:BucketIAMBinding  pulumi-demo-iam-biding                 created     
    +   ├─ gcp:storage:BucketObject      index.html                             created     
    +   ├─ gcp:storage:BucketObject      style.css                              created     
    +   ├─ gcp:storage:BucketObject      image.jpg                              created     
    +   ├─ aws:s3:BucketObject           index.html                             created     
    +   ├─ aws:s3:BucketObject           style.css                              created     
    +   └─ aws:s3:BucketObject           image.jpg                              created     
    
    Outputs:
        gcs_bucket_endpoint: "http://storage.googleapis.com/pulumi-demo-*****/index.html"
        s3_bucket_endpoint : "http://pulumi-demo-*****.s3-website-us-west-2.amazonaws.com/index.html"

    Resources:
        + 10 created

    Duration: 9s
    ```

1. Open the both site URLs in a browser to see both the rendered HTML:

    ```bash
    $ pulumi stack output gcs_bucket_endpoint
    http://storage.googleapis.com/pulumi-demo-*****/index.html

    $ pulumi stack output s3_bucket_endpoint
    http://pulumi-demo-*****.s3-website-us-west-2.amazonaws.com/index.html
    ```

1. To clean up resources, run `pulumi destroy` and answer the confirmation question at the prompt.