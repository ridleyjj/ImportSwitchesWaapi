import sys
import os
from src.Switch_Utils import create_switch_group_with_values

print(f"{sys.argv}\n")

main_folder_path = sys.argv[1]

# a dict of switchGroupName -> switchName[] for creating switches
switch_dict = {}

# a dict of event_name -> dict(switchGroupName -> )
event_dict = {}

def search_for_switches(switch_group_name, switch_group_path):
    for switch_name_list in os.listdir(switch_group_path):
        switch_path = os.path.join(switch_group_path, switch_name_list)
        if os.path.isdir(switch_path):
            switch_name_list = switch_name_list.split(',')
            for switchName in switch_name_list:    
                print('Found switch: ' + switchName + ' adding to switch group...')
                switch_dict[switch_group_name].append(switchName)

def search_for_switch_groups(event_name_path):
    for switch_group_name in os.listdir(event_name_path):
        switch_group_path = os.path.join(event_name_path, switch_group_name)
        if os.path.isdir(switch_group_path):
            print('Found switch group ' + switch_group_name)
            print('Adding switch group name to dict if doesn\'t already exist...')
            switch_dict.setdefault(switch_group_name, [])
            search_for_switches(switch_group_name, switch_group_path)
            

def search_for_events(event_name):
    event_name_path = os.path.join(main_folder_path, event_name)
    if os.path.isdir(event_name_path):
        print('Found event folder: ' + event_name)
        search_for_switch_groups(event_name_path)
        

if os.path.exists(main_folder_path) & os.path.isdir(main_folder_path):
    print('Searching location: ' + main_folder_path + ' for folders...')
    for event_name in os.listdir(main_folder_path):
        search_for_events(event_name)

    print(f"\n### Switches have been searched, found {switch_dict} ###\n")
                    

for key, value in switch_dict.items():
    create_switch_group_with_values(key, value)
