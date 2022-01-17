# Deploy CrossGaurd rule

This sample shows how CrossGuard prohibits tbe deployments which don't follow the deployment rule. As demonstration, define the following rules and show each demo.

- Prohibit the deployment of S3 public bucket
- Prohibit the deployment of EC2 instance which has security group including SSH full open rule

## Deploying and running the program

### Set up Pulumi Policy
1. Install the dependencies for CrossGuard

    ```bash
    $ python -m venv ./venv
    $ ./venv/bin/python -m pip install --upgrade pip setuptools wheel
    $ ./venv/bin/python -m pip install -r requirements.txt
    ```

### Prohibit the deployment of S3 public bucket
In this example, Amazon S3 bucket which has public read acl will be tried to deploy. However it'll be prohibited because CrossGuard policy has the rule to prohibit the deployment of public read or write S3 bucket.

1. Create a new stack:

    ```bash
    $ cd public-s3
    $ pulumi stack init public-s3
    ```

1. Set the AWS region:

    ```bash
    $ pulumi config set aws:region us-west-2
    ```

1. Deploy S3 bucket with CrossGuard policy pack. The deployment will be failed along with the policy rule and the policy violation message will be shown.

    ```bash
    $ pulumi up --policy-pack ../
    Previewing update (public-s3)

    View Live: https://app.pulumi.com/XXXXX/public-s3/public-s3/previews/xxxxxxxxxxxxx

        Type                 Name                 Plan       Info
    +   pulumi:pulumi:Stack  public-s3-public-s3  create     1 error
    +   └─ aws:s3:Bucket     my-bucket            create     
    
    Diagnostics:
    pulumi:pulumi:Stack (public-s3-public-s3):
        error: preview failed
    
    Policy Violations:
        [mandatory]  aws-python v0.0.1  s3-no-public-read (aws:s3/bucket:Bucket: my-bucket)
        Prohibits setting the publicRead or publicReadWrite permission on AWS S3 buckets.
        You cannot set public-read or public-read-write on an S3 bucket. Read more about ACLs here: https://docs.aws.amazon.com/AmazonS3/latest/dev/acl-overview.html
    ```

1. To clean up resources, run `pulumi destroy` and answer the confirmation question at the prompt.

### Prohibit the deployment of EC2 instance that security group including SSH full open rule is attached
In this example, Amazon EC2 instance that security group including SSH full open rule is attached will be tried to deploy. However it'll be prohibited because CrossGuard policy has the rule to prohibit to deploy EC2 instance with SSH full open.

1. Create a new stack:

    ```bash
    $ cd ec2-ssh-full-open
    $ pulumi stack init ec2-ssh-full-open
    ```

1. Set the AWS region:

    ```bash
    $ pulumi config set aws:region us-west-2
    ```

1. Deploy EC2 instance with CrossGuard policy pack. The deployment will be failed along with the policy rule and the policy violation message will be shown.

    ```bash
    $ pulumi up --policy-pack ../
    Previewing update (ec2-ssh-full-open)

    View Live: https://app.pulumi.com/XXXXX/ec2-ssh-full-open/ec2-ssh-full-open/previews/xxxxxxxxxxxxxxxxx

        Type                      Name                                 Plan       
    +   pulumi:pulumi:Stack       ec2-ssh-full-open-ec2-ssh-full-open  create     
    +   ├─ aws:ec2:Vpc            vpc                                  create     
    +   ├─ aws:ec2:Subnet         subnet                               create     
    +   ├─ aws:ec2:SecurityGroup  security-group                       create     
    +   └─ aws:ec2:Instance       ec2                                  create     
    
    Policy Violations:
        [advisory]  aws-python v0.0.1  ec2-no-ssh-full-open (aws:ec2/instance:Instance: ec2)
        can't run policy 'ec2-no-ssh-full-open' during preview: string value at .vpcSecurityGroupIds.0 can't be known during preview
        
    Do you want to perform this update? yes
    Updating (ec2-ssh-full-open)

    View Live: https://app.pulumi.com/XXXXXXX/ec2-ssh-full-open/ec2-ssh-full-open/updates/1

        Type                      Name                                 Status      
    +   pulumi:pulumi:Stack       ec2-ssh-full-open-ec2-ssh-full-open  created     
    +   ├─ aws:ec2:Vpc            vpc                                  created     
    +   ├─ aws:ec2:Subnet         subnet                               created     
    +   └─ aws:ec2:SecurityGroup  security-group                       created     
    
    Policy Violations:
        [mandatory]  aws-python v0.0.1  ec2-no-ssh-full-open (aws:ec2/instance:Instance: ec2)
        Prohibits attaching security group which has the SSH full open rule to EC2 instance. 
        You cannot attach security group which has the SSH full open rule to EC2 instance. 
        
        [mandatory]  aws-python v0.0.1  ec2-no-ssh-full-open (aws:ec2/instance:Instance: ec2)
        Prohibits attaching security group which has the SSH full open rule to EC2 instance. 
        You cannot attach security group which has the SSH full open rule to EC2 instance. 
    ```

1. To clean up resources, run `pulumi destroy` and answer the confirmation question at the prompt.