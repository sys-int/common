import json
from typing import Any, Dict, List

import pulumi
import pulumi_aws as aws


class S3Bucket(pulumi.ComponentResource):
    bucket: aws.s3.Bucket
    policy: aws.iam.Policy

    def __init__(self, name, allowed_ip_addresses: List[str], opts=None):
        super().__init__("sys-int:storage:S3Bucket", f"s3-bucket-{name}", None, opts)
        self.bucket = self.createBucket(name)
        self.policy = self.createPolicy(name, allowed_ip_addresses)

    def createBucket(self, bucket_name: str) -> aws.s3.Bucket:
        bucket = aws.s3.Bucket(bucket_name)
        return bucket

    def createPolicy(self, bucket_name: str, allowed_ip_addresses: List[str]) -> aws.iam.Policy:
        policy_co_create: Dict[str, Any] = {
            "Id": "SourceIP",
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "SourceIP",
                    "Action": "s3:*",
                    "Effect": "Deny",
                    "Resource": [
                        f"arn:aws:s3:::${bucket_name}",
                        f"arn:aws:s3:::${bucket_name}/*",
                    ],
                    "Condition": {"NotIpAddress": {"aws:SourceIp": []}},
                    "Principal": "*",
                }
            ],
        }
        policy_co_create["Statement"][0]["Condition"]["NotIpAddress"]["aws:SourceIp"] = allowed_ip_addresses

        print(policy_co_create)
        policy = aws.iam.Policy(
            f"policy-${bucket_name}",
            name=f"access_policy-${bucket_name}",
            path="/",
            description=f"Access policy ${bucket_name}",
            policy=json.dumps(policy_co_create),
        )
        return policy
