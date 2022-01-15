import pulumi_aws as aws
import pulumi_terraform as terraform

# Reference the Terraform state file:
network_state = terraform.state.RemoteStateReference('network',
    backend_type='local',
    args=terraform.state.LocalBackendArgs(path='./terraform/terraform.tfstate'))

# Read the VPC and subnet IDs into variables:
public_subnet_ids = network_state.get_output('public_subnet_ids')

# Now spin up servers in the first two subnets:
for i in range(3):
    aws.ec2.Instance(f'instance-{i}',
        ami='ami-066333d9c572b0680',
        instance_type='t3.nano',
        subnet_id=public_subnet_ids[i])