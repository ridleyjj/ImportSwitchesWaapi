from waapi import WaapiClient
from src.WwiseUtils import create_object_with_type_and_name
from src.WwiseUtils import is_existing_object_by_type_and_name
from src.WwiseUtils import import_audio_files_as_random_container_within_switch_container
from src.WwiseUtils import add_switch_group_to_switch_container
from src.WwiseUtils import get_object_id_by_type_and_name
from src.WwiseUtils import get_current_switch_group_for_switch_container
from src.WwiseUtils import add_switch_assignment_to_switch_container_child

def create_switch_group_with_values(switch_group_name, switch_values=[], parent_path="\\Switches\\Default Work Unit"):
    with WaapiClient() as client:
        if not is_existing_object_by_type_and_name(client, "SwitchGroup", switch_group_name):
            create_object_with_type_and_name(client, "SwitchGroup", switch_group_name, parent_path)

        for switch_value in switch_values:
            if not is_existing_object_by_type_and_name(client, "Switch", switch_value):
                create_object_with_type_and_name(client, "Switch", switch_value, f"{parent_path}\\{switch_group_name}")

    print(f"\n### SwitchGroup {switch_group_name} has been created with given values. ###\n")

def create_switch_containers_for_events(event_dict, parent_path="\\Actor-Mixer Hierarchy\\Default Work Unit"):
    with WaapiClient() as client:
        for event_name, switch_group_dict in event_dict.items():
            for switch_group_name, switch_dict in switch_group_dict.items():
                switch_container_name = f"{event_name}_{switch_group_name}"

                if not is_existing_object_by_type_and_name(client, "SwitchContainer", switch_container_name):
                    create_object_with_type_and_name(client, "SwitchContainer", switch_container_name, parent_path)
                    
                if len(get_current_switch_group_for_switch_container(client, switch_container_name)) == 0:
                    add_switch_group_to_switch_container(client, switch_container_name, switch_group_name)
                
                for switch_name, audio_files_set in switch_dict.items():
                    switch_id = get_object_id_by_type_and_name(client, "Switch", switch_name)
                    rand_container_name = f"{event_name}_{switch_name}"
                    import_audio_files_as_random_container_within_switch_container(client, audio_files_set, switch_container_name, rand_container_name)
                    add_switch_assignment_to_switch_container_child(client, f"{parent_path}\\{switch_container_name}\\{rand_container_name}", switch_id)




        

    