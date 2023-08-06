

from api_to_yaml.clients.mod import clients
from api_to_yaml.create.aws_appmesh import AppMeshController
from api_to_yaml.create.mod import ECSServiceController
from api_to_yaml.operators.mod import add_items_quantity, metadata_to_args, override, remove_fields, to_args, transform, with_args, with_default, with_tags
import api_to_yaml.create.aws_elbv2_create as elbv2_create
import api_to_yaml.update.aws_iam_update as iam_update
import api_to_yaml.update.ghe_update as ghe_update
import api_to_yaml.create.aws_secretsmanager as secretsmanager_client
import api_to_yaml.update.aws_sg_update as sg_update

ecs = clients["ecs"]
task_set_ecs = ECSServiceController()
elbv2 = clients["elbv2"]
ec2 = clients["ec2"]
iam = clients["iam"]
appmesh = clients["appmesh"]
# Custom app mesh client, just for virtual router and route
custom_appmesh = AppMeshController()
servicediscovery = clients["servicediscovery"]
app_scaling = clients["application-autoscaling"]
asg = clients['asg']
sqs = clients['sqs']
lambda_aws = clients['lambda']
cloudwatch = clients['cloudwatch']
cloudfront = clients['cloudfront']


def update_service_tags(serviceArn, wanted_tags):
    key = 'key'
    tag_key = 'tags'
    current_tags = ecs.list_tags_for_resource(resourceArn=serviceArn).get(
        tag_key, [])
    tags = [i for i in wanted_tags if i not in current_tags]
    tags_keys = [i[key] for i in tags]
    untags_keys = [
        i[key] for i in current_tags
        if i not in wanted_tags and i[key] not in tags_keys
    ]
    if tags:
        ecs.tag_resource(resourceArn=serviceArn, tags=tags)
    if untags_keys:
        ecs.untag_resource(resourceArn=serviceArn, tagKeys=untags_keys)

    return []  # [] means no execute update


def update(kind, content, info, current, resource_path):
    switch = {
        "TaskDefinition": (ecs, "register_task_definition", [
            to_args,
            with_tags(capitalize=False, info=info),
            with_default({
                "family":
                override(info["name"],
                         content.get("metadata", {}).get("family"))
            })
        ], None),
        "TargetGroup": (elbv2, "modify_target_group", [
            to_args,
            with_tags(capitalize=True, info=info),
            with_default({"TargetGroupArn": current.get("TargetGroupArn")}),
            remove_fields(
                ["Name", "VpcId", "Tags", "Port", "Protocol", "TargetType"])
        ], None),
        "Service": (task_set_ecs, "update_service", [
            to_args,
            with_default({
                "cluster":
                info.get("ecs_cluster"),
                "service":
                override(info["name"],
                         content.get("metadata", {}).get("serviceName"))
            })
        ], lambda res: update_service_tags(
            res['service']['serviceArn'],
            with_tags(capitalize=False, info=info)
            (to_args(content)).get("tags", []))),
        "LoadBalancer": (elbv2_create, "update_load_balancer", [
            with_args({
                "kind": kind,
                "content": content,
                "info": info,
                "current": current
            }),
            elbv2_create.alb_canary_config_hook(resource_path)
        ], None),
        "SecurityGroup": (sg_update, "update_security_group", [
            lambda _: {
                "egress":
                (current["GroupId"], "egress", content.get("spec", {}).get(
                    "egress"), current["IpPermissionsEgress"],
                 filter(lambda one: one["IsEgress"], current["Rules"])),
                "ingress":
                (current["GroupId"], "ingress", content.get("spec", {}).get(
                    "ingress"), current["IpPermissions"],
                 filter(lambda one: not one["IsEgress"], current["Rules"])),
                "tags":
                current.get("metadata", {}).get("tags", {})
            }
        ], None),
        "Role": (iam_update, "update_role", [
            with_args({
                "kind": kind,
                "content": content,
                "info": info,
                "current": current
            })
        ], None),
        "Repo": (ghe_update, "update_repo", [
            with_args({
                "kind": kind,
                "content": content,
                "info": info,
                "current": current
            })
        ], None),
        "Mesh": (appmesh, "update_mesh", [
            metadata_to_args,
            remove_fields(["tags"]),
            with_default({"spec": content.get("spec")})
        ], None),
        "VirtualNode": (appmesh, "update_virtual_node", [
            metadata_to_args,
            remove_fields(["tags"]),
            with_default({
                "spec": content.get("spec"),
            })
        ], None),
        "VirtualRouter": (custom_appmesh, "update_virtual_router", [
            metadata_to_args,
            remove_fields(["tags"]),
            with_default({
                "spec": content.get("spec"),
            })
        ], None),
        "Route": (appmesh, "update_route", [
            metadata_to_args,
            remove_fields(["tags"]),
            with_default({
                "spec": content.get("spec"),
            })
        ], None),
        "VirtualGateway": (custom_appmesh, "update_virtual_gateway", [
            metadata_to_args,
            remove_fields(["tags"]),
            with_default({
                "spec": content.get("spec"),
            })
        ], None),
        "VirtualGatewayRoute": (appmesh, "update_gateway_route", [
            metadata_to_args,
            remove_fields(["tags"]),
            with_default({
                "spec": content.get("spec"),
            })
        ], None),
        "VirtualService": (appmesh, "update_virtual_service", [
            metadata_to_args,
            remove_fields(["tags"]),
            with_default({
                "spec": content.get("spec"),
            })
        ], None),
        "ServiceDiscoveryService": (servicediscovery, "update_service", [
            lambda _: {
                "Id": current.get("Id", None),
                "Service": {
                    k: v
                    for k, v in {
                        "Description":
                        content.get("metadata", {}).get("Description", ""),
                        "DnsConfig":
                        content.get("spec", {}).get("DnsConfig", {}),
                        "HealthCheckConfig":
                        content.get("spec", {}).get("HealthCheckConfig", None)
                    }.items() if v is not None
                },
            }
        ], None),
        "Secret": (secretsmanager_client, "update_secret", [
            to_args,
            with_default({"SecretId": current.get('ARN')}),
            transform("SecretString", lambda val: val.decode(
                "utf-8") if isinstance(val, bytes) else val),
            remove_fields([
                "Name", "Tags",
                "ForceOverwriteReplicaSecret"
            ]),
        ], lambda _: secretsmanager_client.update_secret_tags(
            current,
            with_tags(capitalize=True, info=info)
            (to_args(content)).get("Tags", []))),
        # "ScalableTarget":
        # (methods, "create",
        #  [with_args({
        #      "kind": kind,
        #      "content": content,
        #      "info": info
        #  })], None),
        "AutoScalingGroup": (asg, "update_auto_scaling_group", [
            to_args,
            remove_fields(["Tags"])
        ], None),
        "Distribution": (cloudfront, "update_distribution", [
            to_args,
            add_items_quantity,
            lambda args: {
                "Id": args.pop("Id"),
                "IfMatch": args.pop("ETag"),
                "DistributionConfig": args
            }
        ], None),
        "CachePolicy": (cloudfront, "update_cache_policy", [
            to_args,
            add_items_quantity,
            lambda args: {
                "Id": args.pop("Id"),
                "IfMatch": args.pop("ETag"),
                "CachePolicyConfig": args
            }
        ], None),
    }
    if kind in switch:
        client, method, steps, hook = switch[kind]
        func = getattr(client, method)
        args = content
        for step in steps:
            args = step(args)
        res = func(**args)
        if hook:
            args = hook(res)
            return [update(*arg) for arg in args if arg[1]]
        return res
    else:
        raise "Don't know how to update"
