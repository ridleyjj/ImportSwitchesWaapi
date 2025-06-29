import sys
from src.SwitchUtils import create_switch_group_with_values
from src.SwitchUtils import create_switch_containers_for_events
from src.FolderSearching import search_folder_for_switches_and_events

print(f"{sys.argv}\n")

main_folder_path = sys.argv[1]       

switch_dict, event_dict = search_folder_for_switches_and_events(main_folder_path)

for key, value in switch_dict.items():
    create_switch_group_with_values(key, value)

create_switch_containers_for_events(event_dict)
