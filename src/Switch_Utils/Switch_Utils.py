from waapi import WaapiClient
import json

def is_existing_object_by_type_and_name(client, type, name):
    print(f"Checking for existing {type} with name {name}...")
    matching_object = client.call("ak.wwise.core.object.get", {
                "waql": f'$from type {type} where name : "{name}"'
            })["return"]
    
    if len(matching_object) > 0:
        print(f"Found existing {type} with name {name}")
        return True

    print(f"Did not find existing {type} with name {name}")
    return False

def is_existing_switch_group(client, switch_group_name):
    return is_existing_object_by_type_and_name(client, "SwitchGroup", switch_group_name)

def is_existing_switch_value(client, switch_name):
    return is_existing_object_by_type_and_name(client, "Switch", switch_name)

def create_object_with_type_and_name(client, type, name, parent_path):
    print(f"Creating new {type} with name {name}...")
    create_args = {
        "parent": parent_path,
        "type": type,
        "name": name
    }

    options = {
        "onNameConflict": "fail"
    }

    result = client.call("ak.wwise.core.object.create", create_args, options)
    print ( json.dumps(result, indent=4) )

def create_switch_with_name(client, switch_name, parent_path):
    create_object_with_type_and_name(client, "Switch", switch_name, parent_path)

def create_switch_group_with_name(client, switch_group_name, parent_path):
    create_object_with_type_and_name(client, "SwitchGroup", switch_group_name, parent_path)

def create_switch_group_with_values(switch_group_name, switch_values=[], parent_path="\\Switches\\Default Work Unit"):
    with WaapiClient() as client:
        if not is_existing_switch_group(client, switch_group_name):
            create_switch_group_with_name(client, switch_group_name, parent_path)

        for switch_value in switch_values:
            if not is_existing_switch_value(client, switch_value):
                create_switch_with_name(client, switch_value, f"{parent_path}\\{switch_group_name}")

    print(f"\n### SwitchGroup {switch_group_name} has been created with given values. ###\n")


        

    