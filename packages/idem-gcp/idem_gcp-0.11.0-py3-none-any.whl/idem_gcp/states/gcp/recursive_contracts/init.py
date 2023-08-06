import copy

LIST_RESOURCES_WITH_WRAPPER = [
    "gcp.compute.instance",
    "gcp.compute.disk",
    "gcp.compute.forwarding_rule",
]


async def call_present(hub, ctx):
    name = ctx.kwargs.get("name", None)
    state_ctx = ctx.kwargs.get("ctx")
    assert state_ctx, f"state context is missing: {state_ctx}"

    result = {
        "result": True,
        "old_state": None,
        "new_state": None,
        "name": name,
        "comment": [],
    }

    gcp_service_resource_type = state_ctx.get("tag").split("_|")[0]
    # TODO: This if needs to be removed once all resources follow the contract
    if gcp_service_resource_type not in LIST_RESOURCES_WITH_WRAPPER:
        return await ctx.func(*ctx.args, **ctx.kwargs)
    service_resource_type = gcp_service_resource_type.replace("gcp.", "")
    resource_type_camel = hub.tool.gcp.case.camel(
        gcp_service_resource_type.split(".")[-1]
    )

    resource_path = service_resource_type.split(".")
    hub_ref_exec = hub.exec.gcp
    for resource_path_segment in resource_path:
        hub_ref_exec = hub_ref_exec[resource_path_segment]

    resource_id = (
        (ctx.kwargs.get("resource_id") or {})
        or (state_ctx.get("old_state") or {}).get("resource_id")
        or (state_ctx.get("rerun_data") or {}).get("resource_id")
    )

    get_resource_only_with_resource_id = hub.OPT.idem.get(
        "get_resource_only_with_resource_id", False
    )
    if state_ctx.get("rerun_data"):
        handle_operation_ret = await hub.tool.gcp.operation_utils.handle_operation(
            state_ctx,
            state_ctx.get("rerun_data").get("operation_id"),
            service_resource_type,
        )

        if not handle_operation_ret["result"]:
            result["comment"] += handle_operation_ret["comment"]
            result["rerun_data"] = (
                state_ctx.get("rerun_data")
                if handle_operation_ret.get("rerun_data")
                else None
            )
            return result

        resource_id = handle_operation_ret["resource_id"]

    if resource_id:
        old_get_ret = await hub_ref_exec.get(state_ctx, resource_id=resource_id)

        if not old_get_ret["result"] or (
            not old_get_ret["ret"]
            and (state_ctx.get("rerun_data") or get_resource_only_with_resource_id)
        ):
            result["result"] = False
            result["comment"] += old_get_ret["comment"]
            return result

        # long-running operation has succeeded - both update and create
        if state_ctx.get("rerun_data"):
            result["new_state"] = old_get_ret["ret"]
            result["old_state"] = state_ctx.get("rerun_data").get("old_state")
            if result["old_state"]:
                result["comment"].append(
                    hub.tool.gcp.comment_utils.update_comment(
                        gcp_service_resource_type, name
                    )
                )
            else:
                result["comment"].append(
                    hub.tool.gcp.comment_utils.create_comment(
                        gcp_service_resource_type, name
                    )
                )
            return result

        result["old_state"] = old_get_ret["ret"]
    elif not get_resource_only_with_resource_id:
        project = hub.tool.gcp.utils.get_project_from_account(
            state_ctx, ctx.kwargs.get("project")
        )
        local_params = {**ctx.kwargs, "project": project}
        local_params.update({resource_type_camel: name})
        resource_id = hub.tool.gcp.resource_prop_utils.construct_resource_id(
            service_resource_type, local_params
        )
        old_get_ret = await hub_ref_exec.get(state_ctx, resource_id=resource_id)

        if not old_get_ret["result"]:
            result["result"] = False
            result["comment"] += old_get_ret["comment"]
            return result

        if old_get_ret["ret"]:
            result["old_state"] = old_get_ret["ret"]

    state_ctx["wrapper_result"] = copy.deepcopy(copy.copy(result))
    return await ctx.func(*ctx.args, **{**ctx.kwargs, "resource_id": resource_id})
