"""Google Cloud Platform firewalls state module.

Copyright (c) 2023 VMware, Inc. All Rights Reserved.
SPDX-License-Identifier: Apache-2.0

"""
import copy
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List

__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    name: str,
    project: str = None,
    request_id: str = None,
    id_: str = None,
    target_tags: List[str] = None,
    source_service_accounts: List[str] = None,
    denied: List[
        Dict[
            str,
            make_dataclass(
                "items",
                [
                    ("IPProtocol", str, field(default=None)),
                    ("ports", List[str], field(default=None)),
                ],
            ),
        ]
    ] = None,
    description: str = None,
    direction: str = None,
    destination_ranges: List[str] = None,
    allowed: List[
        Dict[
            str,
            make_dataclass(
                "items",
                [
                    ("ports", List[str], field(default=None)),
                    ("IPProtocol", str, field(default=None)),
                ],
            ),
        ]
    ] = None,
    disabled: bool = None,
    self_link: str = None,
    network: str = None,
    priority: int = None,
    log_config: Dict[str, Any] = None,
    target_service_accounts: List[str] = None,
    creation_timestamp: str = None,
    source_tags: List[str] = None,
    source_ranges: List[str] = None,
    kind: str = "compute#firewall",
    resource_id: str = None,
) -> Dict[str, Any]:
    r"""Creates or updates a firewall rule in the specified project using the data included in the request.

    Args:
        name(str): An Idem name of the resource.
        project(str, Optional): Project ID for this request.
        id_(str, Optional):
            [Output Only] The unique identifier for the resource. This identifier is defined by the server. Defaults to None.
        target_tags(List[str], Optional):
            A list of tags that controls which instances the firewall rule applies to. If targetTags are specified,
            then the firewall rule applies only to instances in the VPC network that have one of those tags. If no
            targetTags are specified, the firewall rule applies to all instances on the specified network. Defaults to None.
        source_service_accounts(List[str], Optional):
            If source service accounts are specified, the firewall rules apply only to traffic originating from an
            instance with a service account in this list. Source service accounts cannot be used to control traffic to
            an instance's external IP address because service accounts are associated with an instance, not an IP
            address. sourceRanges can be set at the same time as sourceServiceAccounts. If both are set, the firewall
            applies to traffic that has a source IP address within the sourceRanges OR a source IP that belongs to an
            instance with service account listed in sourceServiceAccount. The connection does not need to match both
            fields for the firewall to apply. sourceServiceAccounts cannot be used at the same time as sourceTags or
            targetTags. Defaults to None.
        denied(list[Dict[str, Dict[str, Any]]], optional):
            The list of DENY rules specified by this firewall. Each rule specifies a protocol and port-range tuple that
            describes a denied connection. Defaults to None.
            * IPProtocol (str, Optional): The IP protocol to which this rule applies. The protocol type is required when
                creating a firewall rule. This value can either be one of the following well known protocol strings
                (tcp, udp, icmp, esp, ah, ipip, sctp) or the IP protocol number.
            * ports (list[str], Optional): An optional list of ports to which this rule applies. This field is only
                applicable for the UDP or TCP protocol. Each entry must be either an integer or a range. If not specified,
                this rule applies to connections through any port. Example inputs include: ["22"], ["80","443"], and
                ["12345-12349"].
        description(str, Optional):
            An optional description of this resource. Provide this field when you create the resource. Defaults to None.
        direction(str, Optional):
            Direction of traffic to which this firewall applies, either `INGRESS` or `EGRESS`. The default is `INGRESS`.
            For `EGRESS` traffic, you cannot specify the sourceTags fields. Defaults to None.
        destination_ranges(List[str], Optional):
            If destination ranges are specified, the firewall rule applies only to traffic that has destination IP
            address in these ranges. These ranges must be expressed in CIDR format. Both IPv4 and IPv6 are supported.
            Defaults to None.
        allowed(List[Dict[str, Dict[str, Any]]], Optional):
            The list of ALLOW rules specified by this firewall. Each rule specifies a protocol and port-range tuple that
            describes a permitted connection. Defaults to None.
            * ports (List[str], Optional): An optional list of ports to which this rule applies. This field is only
                applicable for the UDP or TCP protocol. Each entry must be either an integer or a range. If not specified,
                this rule applies to connections through any port. Example inputs include: ["22"], ["80","443"], and ["12345-12349"].
            * IPProtocol (str, Optional): The IP protocol to which this rule applies. The protocol type is required when
                creating a firewall rule. This value can either be one of the following well known protocol strings
                (tcp, udp, icmp, esp, ah, ipip, sctp) or the IP protocol number.
        disabled(bool, Optional):
            Denotes whether the firewall rule is disabled. When set to true, the firewall rule is not enforced and the
            network behaves as if it did not exist. If this is unspecified, the firewall rule will be enabled. Defaults to None.
        self_link(str, Optional):
            [Output Only] Server-defined URL for the resource. Defaults to None.
        network(str, Optional):
            URL of the network resource for this firewall rule. If not specified when creating a firewall rule, the
            default network is used: global/networks/default If you choose to specify this field, you can specify the
            network as a full or partial URL. For example, the following are all valid
            URLs: - https://www.googleapis.com/compute/v1/projects/myproject/global/networks/my-network -
            projects/myproject/global/networks/my-network - global/networks/default . Defaults to None.
        priority(int, Optional):
            Priority for this rule. This is an integer between `0` and `65535`, both inclusive. The default value is
            `1000`. Relative priorities determine which rule takes effect if multiple rules apply. Lower values indicate
            higher priority. For example, a rule with priority `0` has higher precedence than a rule with priority `1`.
            DENY rules take precedence over ALLOW rules if they have equal priority. Note that VPC networks have implied
            rules with a priority of `65535`. To avoid conflicts with the implied rules, use a priority number less than
            `65535`. Defaults to None.
        log_config(Dict[str, Any], Optional):
            This field denotes the logging options for a particular firewall rule. If logging is enabled, logs will be
            exported to Cloud Logging. Defaults to None.
        target_service_accounts(List[str], Optional):
            A list of service accounts indicating sets of instances located in the network that may make network
            connections as specified in allowed[]. targetServiceAccounts cannot be used at the same time as targetTags
            or sourceTags. If neither targetServiceAccounts nor targetTags are specified, the firewall rule applies to
            all instances on the specified network. Defaults to None.
        creation_timestamp(str, Optional):
            [Output Only] Creation timestamp in RFC3339 text format. Defaults to None.
        source_tags(List[str], Optional):
            If source tags are specified, the firewall rule applies only to traffic with source IPs that match the
            primary network interfaces of VM instances that have the tag and are in the same VPC network. Source tags
            cannot be used to control traffic to an instance's external IP address, it only applies to traffic between
            instances in the same virtual network. Because tags are associated with instances, not IP addresses. One or
            both of sourceRanges and sourceTags may be set. If both fields are set, the firewall applies to traffic that
            has a source IP address within sourceRanges OR a source IP from a resource with a matching tag listed in the
            sourceTags field. The connection does not need to match both fields for the firewall to apply. Defaults to None.
        source_ranges(List[str], Optional):
            If source ranges are specified, the firewall rule applies only to traffic that has a source IP address in
            these ranges. These ranges must be expressed in CIDR format. One or both of sourceRanges and sourceTags may
            be set. If both fields are set, the rule applies to traffic that has a source IP address within sourceRanges
            OR a source IP from a resource with a matching tag listed in the sourceTags field. The connection does not
            need to match both fields for the rule to apply. Both IPv4 and IPv6 are supported. Defaults to None.
        kind(str, Optional):
            [Output Only] Type of the resource. Always compute#firewall for firewall rules. Defaults to "compute#firewall".
        resource_id(str, Optional):
            An identifier of the resource in the provider. Defaults to None.

    Returns:
        Dict[str, Any]

    Examples:

        .. code-block:: sls

            firewall-present:
              gcp.compute.firewall.present:
              - name: my-firewall-name
              - description: Free text description
              - network: https://www.googleapis.com/compute/v1/projects/project-name/global/networks/default
              - source_ranges:
                - 0.0.0.0/0
              - allowed:
                - ip_protocol: tcp
                  ports:
                  - '22'
              - direction: INGRESS
              - log_config:
                  enable: false
              - disabled: false
    """

    result = {
        "result": True,
        "old_state": None,
        "new_state": None,
        "name": name,
        "comment": [],
    }

    project = hub.tool.gcp.utils.get_project_from_account(ctx, project)

    if ctx.get("rerun_data"):
        handle_operation_ret = await hub.tool.gcp.operation_utils.handle_operation(
            ctx, ctx.get("rerun_data").get("operation_id"), "compute.firewall"
        )

        if not handle_operation_ret["result"]:
            result["result"] = False
            result["comment"] += handle_operation_ret["comment"]
            result["rerun_data"] = ctx.get("rerun_data")
            return result

        resource_id = handle_operation_ret["resource_id"]

    get_resource_only_with_resource_id = hub.OPT.idem.get(
        "get_resource_only_with_resource_id", False
    )
    if resource_id:
        old_get_ret = await hub.exec.gcp.compute.firewall.get(
            ctx, resource_id=resource_id
        )

        if not old_get_ret["result"] or (
            not old_get_ret["ret"] and get_resource_only_with_resource_id
        ):
            result["result"] = False
            result["comment"] += old_get_ret["comment"]
            return result

        # long running operation has succeeded - both update and create
        if ctx.get("rerun_data"):
            result["new_state"] = old_get_ret["ret"]
            result["old_state"] = ctx["rerun_data"]["old_state"]
            if ctx["rerun_data"]["old_state"]:
                result["comment"].append(
                    hub.tool.gcp.comment_utils.update_comment(
                        "gcp.compute.firewall", name
                    )
                )
            else:
                result["comment"].append(
                    hub.tool.gcp.comment_utils.create_comment(
                        "gcp.compute.firewall", name
                    )
                )
            return result

        result["old_state"] = copy.deepcopy(copy.copy(old_get_ret["ret"]))
    elif not get_resource_only_with_resource_id:
        resource_id = hub.tool.gcp.resource_prop_utils.construct_resource_id(
            "compute.firewall", {"project": project, "firewall": name}
        )
        old_get_ret = await hub.exec.gcp.compute.firewall.get(
            ctx, resource_id=resource_id
        )

        if not old_get_ret["result"]:
            result["result"] = False
            result["comment"] += old_get_ret["comment"]
            return result

        if old_get_ret["ret"]:
            result["old_state"] = copy.deepcopy(copy.copy(old_get_ret["ret"]))

    resource_body = {
        "creation_timestamp": creation_timestamp,
        "priority": priority,
        "log_config": log_config,
        "direction": direction,
        "source_ranges": source_ranges,
        "source_service_accounts": source_service_accounts,
        "allowed": allowed,
        "target_tags": target_tags,
        "source_tags": source_tags,
        "denied": denied,
        "target_service_accounts": target_service_accounts,
        "network": network,
        "destination_ranges": destination_ranges,
        "disabled": disabled,
        "name": name,
        "description": description,
    }

    resource_body = {k: v for (k, v) in resource_body.items() if v is not None}
    operation = None
    if result["old_state"]:
        changes = hub.tool.gcp.utils.compare_states(
            result["old_state"], resource_body, "compute.firewall"
        )
        if not changes:
            result["result"] = True
            result["comment"].append(
                hub.tool.gcp.comment_utils.up_to_date_comment(
                    "gcp.compute.firewall", name
                )
            )
            result["new_state"] = {"resource_id": resource_id, **resource_body}
            return result

        if ctx["test"]:
            result["comment"].append(
                hub.tool.gcp.comment_utils.would_update_comment(
                    "gcp.compute.firewall", name
                )
            )
            result["new_state"] = {"resource_id": resource_id, **resource_body}
            return result

        update_ret = await hub.exec.gcp_api.client.compute.firewall.patch(
            hub, ctx, resource_id=resource_id, body=resource_body
        )
        if not update_ret["result"] or not update_ret["ret"]:
            result["result"] = False
            result["comment"] += update_ret["comment"]
            return result

        if hub.tool.gcp.operation_utils.is_operation(update_ret.get("ret")):
            operation = update_ret["ret"]

        get_ret = await hub.exec.gcp.compute.firewall.get(ctx, resource_id=resource_id)
        if not get_ret["result"] and not get_ret["ret"]:
            result["result"] = False
            result["comment"] += get_ret["comment"]
            return result

        result["new_state"] = get_ret["ret"]
        result["comment"].append(
            hub.tool.gcp.comment_utils.update_comment("gcp.compute.firewall", name)
        )
        return result
    else:
        if ctx.get("test", False):
            result["comment"].append(
                hub.tool.gcp.comment_utils.would_create_comment(
                    "gcp.compute.firewall", name
                )
            )
            result["new_state"] = {"resource_id": resource_id, **resource_body}
            return result
        create_ret = await hub.exec.gcp_api.client.compute.firewall.insert(
            ctx, project=project, body=resource_body
        )
        if not create_ret["result"] or not create_ret["ret"]:
            result["result"] = False
            if create_ret["comment"] and next(
                (
                    comment
                    for comment in create_ret["comment"]
                    if "alreadyExists" in comment
                ),
                None,
            ):
                result["comment"].append(
                    hub.tool.gcp.comment_utils.already_exists_comment(
                        "gcp.compute.firewall", name
                    )
                )
            else:
                result["comment"] += create_ret["comment"]
            return result

        if hub.tool.gcp.operation_utils.is_operation(create_ret.get("ret")):
            operation = create_ret["ret"]

    if operation:
        operation_id = hub.tool.gcp.resource_prop_utils.parse_link_to_resource_id(
            operation.get("selfLink"), "compute.global_operation"
        )
        result["rerun_data"] = {
            "operation_id": operation_id,
            "old_state": result["old_state"],
        }
        result["result"] = False
        return result

    return result


async def absent(
    hub,
    ctx,
    name: str,
    project: str = None,
    request_id: str = None,
    resource_id: str = None,
) -> Dict[str, Any]:
    r"""Deletes the specified firewall.

    Args:
        name(str): Name of the firewall rule to return.
        project(str, Optional): Project ID for this request.
        request_id(str, Optional): An optional request ID to identify requests. Specify a unique request ID so that if
            you must retry your request, the server will know to ignore the request if it has already been completed.
            For example, consider a situation where you make an initial request and the request times out. If you make
            the request again with the same request ID, the server can check if original operation with the same request
            ID was received, and if so, will ignore the second request. This prevents clients from accidentally creating
            duplicate commitments. The request ID must be a valid UUID with the exception that zero UUID is not
            supported ( 00000000-0000-0000-0000-000000000000). Defaults to None.
        resource_id(str, Optional):
            An identifier of the resource in the provider. Defaults to None.

    Returns:
        Dict[str, Any]

    Examples:

        .. code-block:: sls

            resource_is_absent:
              gcp.compute.firewall.absent:
                - name: value
                - project: value
                - firewall: value
    """

    result = {
        "result": True,
        "old_state": None,
        "new_state": None,
        "name": name,
        "comment": [],
    }

    project = hub.tool.gcp.utils.get_project_from_account(ctx, project)
    if not resource_id and not hub.OPT.idem.get(
        "get_resource_only_with_resource_id", False
    ):
        resource_id = hub.tool.gcp.resource_prop_utils.construct_resource_id(
            "compute.firewall", {**locals(), "firewall": name}
        )

    if not resource_id:
        result["comment"].append(
            hub.tool.aws.comment_utils.already_absent_comment(
                "gcp.compute.firewall", name
            )
        )
        return result

    if not ctx.get("rerun_data"):
        get_ret = await hub.exec.gcp.compute.firewall.get(ctx, resource_id=resource_id)

        if not get_ret["result"]:
            result["result"] = False
            result["comment"] += get_ret["comment"]
            return result

        if not get_ret["ret"]:
            result["comment"].append(
                hub.tool.gcp.comment_utils.already_absent_comment(
                    "gcp.compute.firewall", name
                )
            )
            return result

        result["old_state"] = get_ret["ret"]

    if ctx["test"]:
        result["comment"].append(
            hub.tool.gcp.comment_utils.would_delete_comment(
                "gcp.compute.firewall", name
            )
        )
        return result

    if not ctx.get("rerun_data"):
        # First iteration; invoke firewall's delete()
        delete_ret = await hub.exec.gcp_api.client.compute.firewall.delete(
            ctx, resource_id=resource_id, request_id=request_id
        )
        if hub.tool.gcp.operation_utils.is_operation(delete_ret.get("ret")):
            result["result"] = False
            result["comment"] += delete_ret["comment"]
            result[
                "rerun_data"
            ] = hub.tool.gcp.resource_prop_utils.parse_link_to_resource_id(
                delete_ret["ret"].get("selfLink"), "compute.global_operation"
            )
            return result
    else:
        # delete() has been called on some previous iteration
        handle_operation_ret = await hub.tool.gcp.operation_utils.handle_operation(
            ctx, ctx.get("rerun_data"), "compute.firewall"
        )
        if not handle_operation_ret["result"]:
            result["result"] = False
            result["comment"] += handle_operation_ret["comment"]
            result["rerun_data"] = handle_operation_ret["rerun_data"]
            return result

    result["comment"].append(
        hub.tool.gcp.comment_utils.delete_comment("gcp.compute.firewall", name)
    )
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    r"""Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    Retrieves the list of firewall rules available to the specified project.

    Returns:
        Dict[str, Any]

    Examples:

        .. code-block:: bash

            $ idem describe gcp.compute.firewall
    """

    result = {}

    describe_ret = await hub.exec.gcp.compute.firewall.list(
        ctx, project=ctx.acct.project_id
    )

    if not describe_ret["result"]:
        hub.log.debug(
            f"Could not describe gcp.compute.firewall {describe_ret['comment']}"
        )
        return result

    for resource in describe_ret["ret"]:
        resource_id = resource.get("resource_id")

        result[resource_id] = {
            "gcp.compute.firewall.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource.items()
            ]
        }

    return result


def is_pending(hub, ret: dict, state: str = None, **pending_kwargs) -> bool:
    return hub.tool.gcp.utils.is_pending(ret=ret, state=state, **pending_kwargs)
