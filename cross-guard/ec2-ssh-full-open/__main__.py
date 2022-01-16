import pulumi_aws as aws

# Create a VPC
vpc = aws.ec2.Vpc("vpc", cidr_block="10.0.0.0/16")

# Create a Subnet
subnet = aws.ec2.Subnet(
    "subnet",
    vpc_id=vpc.id,
    cidr_block="10.0.0.0/24",
    tags={
        "Name": "ssh-full-open",
    })

# Create a Security Group
sg = aws.ec2.SecurityGroup(
    "security-group",
    description="Allow SSH inbound traffic from any place",
    vpc_id=vpc.id,
    ingress=[aws.ec2.SecurityGroupIngressArgs(
        description="SSH",
        from_port=22,
        to_port=22,
        protocol="tcp",
        cidr_blocks=['0.0.0.0/0'],
        ipv6_cidr_blocks=['::/0'],
    )],
    egress=[aws.ec2.SecurityGroupEgressArgs(
        from_port=0,
        to_port=0,
        protocol="-1",
        cidr_blocks=["0.0.0.0/0"],
        ipv6_cidr_blocks=["::/0"],
    )],
    tags={
        "Name": "allow_ssh"
    }
)

# Get an AMI
ami = aws.ec2.get_ami(most_recent=True,
    filters=[
        aws.ec2.GetAmiFilterArgs(
            name="name",
            values=["amzn2-ami-kernel-5.10-hvm-*"],
        ),
        aws.ec2.GetAmiFilterArgs(
            name="virtualization-type",
            values=["hvm"],
        ),
    ],
    owners=["amazon"])

# Create an Instance
ec2 = aws.ec2.Instance(
    "ec2",
    ami=ami.id,
    instance_type="t3.nano",
    tags={
        "Name": "ssh-full-open",
    },
    subnet_id=subnet.id,
    vpc_security_group_ids=[sg.id],
)