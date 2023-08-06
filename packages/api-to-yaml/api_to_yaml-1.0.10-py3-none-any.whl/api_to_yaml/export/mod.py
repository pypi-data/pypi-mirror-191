
import re
from copy import deepcopy
from api_to_yaml.operators.mod import remove_fields, remove_items_quantity, template_fields, to_crd


def export(kind, current, info):
    switch = {"Repo": [remove_fields(["metadata"])],
              "Distribution": [remove_items_quantity,
                               lambda tidied: template_fields(
                                   deepcopy(tidied), ["Origins", "CacheBehaviors"]),
                               lambda content: to_crd(content, "cloudfront.aws.binance/v1alpha1", "Distribution")],
              "CachePolicy": [remove_items_quantity,
                              lambda content: to_crd(
                                  content, "cloudfront.aws.binance/v1alpha1", "CachePolicy")
                              ]
              }
    for func in switch[kind]:
        current = func(current)
    return current


def collect_cache_policy_id_(acc, content, info):
    if type(content) == dict:
        v = content.get("CachePolicyId")
        if v is not None and re.match(r"^\w{8}-\w{4}-\w{4}-\w{4}-\w{12}$", v):
            copied = deepcopy(info)
            copied["cloudfront_type"] = "CachePolicy"
            acc[v] = ("CachePolicy", {"metadata": {"Id": v}}, copied)
        for k, v in content.items():
            collect_cache_policy_id_(acc, v, info)
    elif type(content) == list:
        for one in content:
            collect_cache_policy_id_(acc, one, info)


def collect_cache_policy_id(refs, info):
    def wrap(content):
        collect_cache_policy_id_(refs, content, info)
        return content
    return wrap


def export_ref(kind, current, info):
    refs = {}
    switch = {
        "Distribution": [collect_cache_policy_id(refs, info),
                         remove_items_quantity,
                         lambda tidied: template_fields(
                             deepcopy(tidied), ["Origins", "CacheBehaviors"]),
                         lambda content: to_crd(content, "cloudfront.aws.binance/v1alpha1", "Distribution")],
    }
    if kind in switch:
        for func in switch[kind]:
            current = func(current)
        return refs, current
    else:
        return {}, export(kind, current, info)
