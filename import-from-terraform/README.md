# Deploy EC2 instances in VPC created by Terraform

This sample shows how to deploy EC2 instances in VPC created by Terraform by using [Pulumi](https://www.pulumi.com/)

## Deploying and running the program

1. Create VPC and subnets by Terraform:

    ```bash
    $ cd terraform
    $ terraform init
    $ terraform apply
      .
      .
      .
    Apply complete! Resources: 10 added, 0 changed, 0 destroyed.

    Outputs:

    public_subnet_ids = [
        "subnet-08fbc359df843491d",
        "subnet-0527f016353417344",
        "subnet-0fb66aecc675fa15f",
    ]
    ```

1. Create a new stack:

    ```bash
    $ cd ..
    $ pulumi stack init import-from-terraform
    ```

1. Set the AWS region:

    ```bash
    $ pulumi config set aws:region us-west-2
    ```

1. Run `pulumi up` to preview and deploy changes.  After the preview is shown you will be
    prompted if you want to continue or not.

    ```bash
    $ pulumi up
    Previewing update (import-from-terraform)

    View Live: https://app.pulumi.com/xxxxx/import-from-terraform/import-from-terraform/previews/xxxxxxxxxxxxxxxxxxxx

        Type                 Name                                         Plan       
    +   pulumi:pulumi:Stack  import-from-terraform-import-from-terraform  create     
    +   ├─ aws:ec2:Instance  instance-1                                   create     
    +   ├─ aws:ec2:Instance  instance-0                                   create     
    +   └─ aws:ec2:Instance  instance-2                                   create     
    
    Resources:
        + 4 to create

    Do you want to perform this update? yes
    Updating (import-from-terraform)

    View Live: https://app.pulumi.com/xxxxxx/import-from-terraform/import-from-terraform/updates/1

        Type                 Name                                         Status      
    +   pulumi:pulumi:Stack  import-from-terraform-import-from-terraform  created     
    +   ├─ aws:ec2:Instance  instance-0                                   created     
    +   ├─ aws:ec2:Instance  instance-2                                   created     
    +   └─ aws:ec2:Instance  instance-1                                   created     
    
    Resources:
        + 4 created

    Duration: 17s
    ```

1. To clean up resources, run `pulumi destroy` and answer the confirmation question at the prompt.

1. Clean up resources created by Terraform
    ```
    $ cd terraform
    $ terraform destroy
    ```