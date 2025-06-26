import json

def get_object_id_by_type_and_name(client, type, name):
    matching_objects = client.call("ak.wwise.core.object.get", {
                "waql": f'$from type {type} where name : "{name}"'
            })["return"]
    print(json.dumps(matching_objects, indent=4))
    return matching_objects[0]["id"]

def find_all_objects_by_type(client, type):
    print(f"Checking for all objects of type: {type}...")
    matching_objects = client.call("ak.wwise.core.object.get", {
                "waql": f'$from type {type}'
            })["return"]
    
    print(json.dumps(matching_objects, indent=4))

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

def create_object_with_type_and_name(client, type, name, parent_path, on_name_conflict="fail"):
    print(f"Creating new {type} with name {name}...")
    create_args = {
        "parent": parent_path,
        "type": type,
        "name": name
    }

    options = {
        "onNameConflict": on_name_conflict
    }

    result = client.call("ak.wwise.core.object.create", create_args, options)
    print ( json.dumps(result, indent=4) )
    return result["id"]

def import_audio_files(client, audio_file_paths, parent_path="\\Actor-Mixer Hierarchy\\Default Work Unit"):
    audio_imports = []
    for audio_file_path in audio_file_paths:
        sound_name_with_extension = audio_file_path.split('\\')[-1]
        sound_name = sound_name_with_extension.split('.')[0]
        audio_imports.append({
            "audioFile": audio_file_path,
            "objectPath": f"{parent_path}\\<Sound SFX>${sound_name}"
        })
    args = {
        "importOperation": "useExisting",
        "default": {
            "importLanguage": "SFX"
        },
        "imports": audio_imports
    }
    options = {
        "return": [
            "id",
            "name",
            "path"
        ]
    }
    result = client.call("ak.wwise.core.audio.import", args, options)
    print(json.dumps(result, indent=4))

def import_audio_files_as_random_container(client, audio_file_paths, random_container_name, parent_path="\\Actor-Mixer Hierarchy\\Default Work Unit"):
    parent_path += f"\\<Random Container>{random_container_name}"
    return import_audio_files(client, audio_file_paths, parent_path)

def import_audio_files_as_random_container_within_switch_container(client, audio_file_paths, switch_container_name, random_container_name, parent_path="\\Actor-Mixer Hierarchy\\Default Work Unit"):
    parent_path += f"\\<Switch Container>{switch_container_name}"
    return import_audio_files_as_random_container(client, audio_file_paths, random_container_name, parent_path)

def add_switch_group_to_switch_container(client, switch_container_name, switch_group_name):
    container_id = get_object_id_by_type_and_name(client, "SwitchContainer", switch_container_name)
    args = {
        "object": container_id,
        "reference": "SwitchGroupOrStateGroup",
        "value": f"SwitchGroup:{switch_group_name}"
    }
    result = client.call("ak.wwise.core.object.setReference", args)

    print(json.dumps(result, indent=4))

def get_current_switch_group_for_switch_container(client, switch_container_name):
    property_value = client.call("ak.wwise.core.object.get", {
                "waql": f'$from type SwitchContainer where name : "{switch_container_name}" select SwitchGroupOrStateGroup'
            })["return"]
    
    print(json.dumps(property_value, indent=4))
    return property_value

def add_switch_assignment_to_switch_container_child(client, child_path, switch_id):
    args = {
        "child": child_path,
        "stateOrSwitch": switch_id
    }
    result = client.call("ak.wwise.core.switchContainer.addAssignment", args)
    json.dumps(result, indent=4)