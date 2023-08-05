#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import yaml
import json
import types
import boto3
import datetime
from functools import partial
from time import sleep
from collections import defaultdict
from api_to_yaml.clients.ghe import GHE


def find_distribution(self, Id=None, Alias=None):
    if Id is None:
        pager = self.get_paginator("list_distributions")
        matched = []
        for res in pager.paginate():
            for dist in res["DistributionList"]["Items"]:
                if Alias in dist["Aliases"].get("Items", []):
                    matched.append(dist)
        if len(matched) == 1:
            Id = matched[0]["Id"]
        elif len(matched) == 0:
            return None
        else:
            raise f"found {len(matched)} distribution with Alias: {Alias}. please specify by Id"
    res = self.get_distribution_config(Id=Id)
    res["DistributionConfig"]["Id"] = Id
    res["DistributionConfig"]["ETag"] = res["ETag"]
    return res


def list_cache_policies_(self):
    marker = None
    while True:
        if marker:
            res = self.list_cache_policies(Marker=marker)
        else:
            res = self.list_cache_policies()
        marker = res["CachePolicyList"].get("NextMarker")
        for one in res["CachePolicyList"]["Items"]:
            one["CachePolicy"]["CachePolicyConfig"]["Id"] = one["CachePolicy"]["Id"]
#             one["CachePolicy"]["CachePolicyConfig"]["Type"] = one["Type"]
            yield one["CachePolicy"]["CachePolicyConfig"]
        if marker is None:
            break


def find_cache_policy(self, Id=None, Name=None):
    if Id is None:
        cache_policies = list(self.list_cache_policies_())
        res = [one for one in cache_policies if one["Name"] == Name]
        if len(res) == 0:
            return None
        Id = res[0]["Id"]
    result = self.get_cache_policy(Id=Id)
    if result is None:
        return None
    Id = result["CachePolicy"]["Id"]
    config = result["CachePolicy"]["CachePolicyConfig"]
    config["Id"] = Id
    config["ETag"] = result["ETag"]
    return config


cloudfront = boto3.client('cloudfront')
cloudfront.find_distribution = types.MethodType(find_distribution, cloudfront)
cloudfront.list_cache_policies_ = types.MethodType(
    list_cache_policies_, cloudfront)
cloudfront.find_cache_policy = types.MethodType(find_cache_policy, cloudfront)

clients = {
    "ecs":
    boto3.client('ecs'),
    "elbv2":
    boto3.client("elbv2"),
    "ec2":
    boto3.client("ec2"),
    "iam":
    boto3.client("iam"),
    "appmesh":
    boto3.client("appmesh"),
    "servicediscovery":
    boto3.client("servicediscovery"),
    "secretsmanager":
    boto3.client("secretsmanager"),
    "ghe":
    GHE(base_url="https://git.toolsfdg.net/api/v3",
        login_or_token=os.getenv('GITHUB_TOKEN')),
    "application-autoscaling":
        boto3.client("application-autoscaling"),
    "sqs":
        boto3.resource('sqs'),
    "lambda":
        boto3.client('lambda'),
    "asg":
        boto3.client('autoscaling'),
    "cloudwatch":
        boto3.client('cloudwatch'),
    "cloudfront":
        cloudfront
}
