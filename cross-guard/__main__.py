import pprint
from typing import Protocol
import boto3

from pulumi_policy import (
    EnforcementLevel,
    PolicyPack,
    ReportViolation,
    ResourceValidationArgs,
    ResourceValidationPolicy,
)

def get_sg_inbound_rules(id):
    sg = boto3.resource('ec2').SecurityGroup(id)
    return sg.ip_permissions

def s3_no_public_read_validator(args: ResourceValidationArgs, report_violation: ReportViolation):
    if args.resource_type == "aws:s3/bucket:Bucket" and "acl" in args.props:
        acl = args.props["acl"]
        if acl == "public-read" or acl == "public-read-write":
            report_violation(
                "You cannot set public-read or public-read-write on an S3 bucket. " +
                "Read more about ACLs here: https://docs.aws.amazon.com/AmazonS3/latest/dev/acl-overview.html")

def ec2_no_ssh_full_open_validator(args: ResourceValidationArgs, report_violation: ReportViolation):
    if args.resource_type == "aws:ec2/instance:Instance" and "vpcSecurityGroupIds" in args.props:
        for id in args.props["vpcSecurityGroupIds"]:
            inbound_rules = get_sg_inbound_rules(id)
            for inbound_rule in inbound_rules:
                from_port = inbound_rule["FromPort"]
                to_port = inbound_rule["ToPort"]
                ipv4_ranges = inbound_rule["IpRanges"]
                ipv6_ranges = inbound_rule["IpRanges"]
                if from_port <= 22 and to_port >= 22:
                    for ipv4_range in ipv4_ranges:
                        if ipv4_range['CidrIp'] == '0.0.0.0/0':
                            report_violation("You cannot attach security group which has the SSH full open rule to EC2 instance. ")
                    for ipv6_range in ipv6_ranges:
                        if ipv6_range['CidrIp'] == '::/0':
                            report_violation("You cannot attach security group which has the SSH full open rule to EC2 instance. ")

s3_no_public_read = ResourceValidationPolicy(
    name="s3-no-public-read",
    description="Prohibits setting the publicRead or publicReadWrite permission on AWS S3 buckets.",
    enforcement_level=EnforcementLevel.MANDATORY,
    validate=s3_no_public_read_validator,
)

ec2_no_ssh_full_open = ResourceValidationPolicy(
    name="ec2-no-ssh-full-open",
    description="Prohibits attaching security group which has the SSH full open rule to EC2 instance. ",
    enforcement_level=EnforcementLevel.MANDATORY,
    validate=ec2_no_ssh_full_open_validator,
)

PolicyPack(
    name="aws-python",
    enforcement_level=EnforcementLevel.MANDATORY,
    policies=[
        s3_no_public_read,
        ec2_no_ssh_full_open,
    ],
)
