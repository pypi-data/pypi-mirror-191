import copy
from typing import Any
from typing import Dict
from typing import List


async def update_network_interfaces(
    hub,
    ctx,
    current_instance: Dict[str, Any],
    new_network_interfaces: List[Dict[str, Any]],
) -> Dict[str, Any]:
    # Update the updatable network interface properties and the access configs
    result = {"result": False, "comment": []}

    existing_network_interfaces = copy.deepcopy(
        current_instance.get("network_interfaces", [])
    )
    for net_intf in new_network_interfaces:
        existing_net_intf = next(
            (
                existing_network_interfaces[idx]
                for idx in range(len(existing_network_interfaces))
                if existing_network_interfaces[idx].get("name") == net_intf.get("name")
            ),
            None,
        )
        if not existing_net_intf:
            break

        # According to documentation, only one access config per instance is supported.

        existing_access_configs = existing_net_intf.get("access_configs", [])
        desired_access_configs = net_intf.get("access_configs", [])

        existing_ac = (
            existing_access_configs[0] if len(existing_access_configs) > 0 else None
        )
        desired_ac = (
            desired_access_configs[0] if len(desired_access_configs) > 0 else None
        )

        if not existing_ac and not desired_ac:
            continue

        elif existing_ac and not desired_ac:
            op_ret = await hub.exec.gcp_api.client.compute.instance.deleteAccessConfig(
                ctx,
                resource_id=current_instance.get("resource_id"),
                access_config=existing_ac.get("name"),
                network_interface=net_intf.get("name"),
            )

            r = await hub.tool.gcp.operation_utils.await_operation_completion(
                ctx, op_ret, "compute.instance", "compute.zone_operation"
            )
            if not r["result"]:
                result["comment"] += r["comment"]
                return result

        elif desired_ac and not existing_ac:
            op_ret = await hub.exec.gcp_api.client.compute.instance.addAccessConfig(
                ctx,
                resource_id=current_instance.get("resource_id"),
                network_interface=net_intf.get("name"),
                body=desired_ac,
            )

            r = await hub.tool.gcp.operation_utils.await_operation_completion(
                ctx, op_ret, "compute.instance", "compute.zone_operation"
            )
            if not r["result"]:
                result["comment"] += r["comment"]
                return result

        # existing_ac and desired_ac
        elif next(
            (
                key
                for key in desired_ac.keys()
                if desired_ac.get(key) != existing_ac.get(key)
            ),
            None,
        ):
            op_ret = await hub.exec.gcp_api.client.compute.instance.updateAccessConfig(
                ctx,
                resource_id=current_instance.get("resource_id"),
                network_interface=net_intf.get("name"),
                body=desired_ac,
            )

            r = await hub.tool.gcp.operation_utils.await_operation_completion(
                ctx, op_ret, "compute.instance", "compute.zone_operation"
            )
            if not r["result"]:
                result["comment"] += r["comment"]
                return result

        # Network interface update
        # Cannot update access config through network interface update function - must be a separate call
        body = hub.tool.gcp.utils.create_dict_body_on_top_of_old(
            ctx, existing_net_intf, net_intf
        )

        # We want to exclude access configs from update nic operation because it is not supported and
        # it is handled separately.
        body.pop("access_configs", None)
        existing_net_intf.pop("access_configs", None)

        if body != existing_net_intf:
            op_ret = (
                await hub.exec.gcp_api.client.compute.instance.updateNetworkInterface(
                    ctx,
                    resource_id=current_instance.get("resource_id"),
                    network_interface=existing_net_intf.get("name"),
                    body=body,
                )
            )

            ret = await hub.tool.gcp.operation_utils.await_operation_completion(
                ctx, op_ret, "compute.instance", "compute.zone_operation"
            )
            if not ret["result"]:
                result["comment"] += ret["comment"]
                return result

    result["result"] = True
    return result


async def update_shielded_instance_config(
    hub,
    ctx,
    shielded_instance_config: Dict[str, bool],
    project: str = None,
    zone: str = None,
    instance: str = None,
    resource_id: str = None,
) -> Dict[str, Any]:
    return await hub.exec.gcp.compute.instance.update_shielded_instance_config(
        ctx,
        shielded_instance_config["enable_secure_boot"],
        shielded_instance_config["enable_vtpm"],
        shielded_instance_config["enable_integrity_monitoring"],
        project,
        zone,
        instance,
        resource_id,
    )


async def update_shielded_instance_integrity_policy(
    hub,
    ctx,
    shielded_instance_integrity_policy: Dict[str, bool],
    project: str = None,
    zone: str = None,
    instance: str = None,
    resource_id: str = None,
) -> Dict[str, Any]:
    return await hub.exec.gcp.compute.instance.set_shielded_instance_integrity_policy(
        ctx,
        shielded_instance_integrity_policy["update_auto_learn_policy"],
        project,
        zone,
        instance,
        resource_id,
    )


async def update_status(
    hub,
    ctx,
    resource_id: str,
    current_status: str,
    desired_status: str,
) -> Dict[str, Any]:

    result = {"result": False, "comment": []}

    states = ["RUNNING", "SUSPENDED", "TERMINATED"]
    if not desired_status in states:
        result["comment"].append(
            f"Incorrect instance status in the request: {desired_status}, must be one of: {states}"
        )
        return result

    # See https://cloud.google.com/compute/docs/instances/instance-life-cycle for instance's state transition diagram

    ret = None
    if current_status in ["PROVISIONING", "STAGING", "RUNNING", "REPAIRING"]:
        if desired_status == "TERMINATED":
            ret = await hub.exec.gcp.compute.instance.stop(ctx, resource_id=resource_id)
        elif desired_status == "SUSPENDED":
            ret = await hub.exec.gcp.compute.instance.suspend(
                ctx, resource_id=resource_id
            )
    elif current_status in ["STOPPING", "TERMINATED"] and desired_status == "RUNNING":
        ret = await hub.exec.gcp.compute.instance.start(ctx, resource_id=resource_id)
    elif current_status in ["SUSPENDING", "SUSPENDED"] and desired_status == "RUNNING":
        ret = await hub.exec.gcp.compute.instance.resume(ctx, resource_id=resource_id)
    else:
        result["comment"].append(
            f"Incorrect instance status transition: {current_status} => {desired_status}"
        )
        return result

    result["result"] = ret["result"]
    result["comment"] += ret["comment"]
    return result
