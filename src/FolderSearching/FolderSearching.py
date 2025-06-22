import os

class FolderSearcher:
    def __init__(self, main_folder_path):
        self.main_folder_path = main_folder_path
        self.switch_dict = {} # a dict of switchGroupName -> switchName[] for creating switches
        self.event_dict = {} # a dict of event_name -> dict(switchGroupName -> )

        if os.path.exists(self.main_folder_path) & os.path.isdir(self.main_folder_path):
            print('Searching location: ' + main_folder_path + ' for folders...')
            for event_name in os.listdir(main_folder_path):
                self.search_for_events(event_name)

            print(f"\n### Switches have been searched, found {self.switch_dict} ###\n")
        else:
            print(f"\nERROR: Location {main_folder_path} not found.\n")

    def search_for_switches(self, switch_group_name, switch_group_path):
        for switch_name_list in os.listdir(switch_group_path):
            switch_path = os.path.join(switch_group_path, switch_name_list)
            if os.path.isdir(switch_path):
                switch_name_list = switch_name_list.split(',')
                for switchName in switch_name_list:    
                    print('Found switch: ' + switchName + ' adding to switch group...')
                    self.switch_dict[switch_group_name].add(switchName)

    def search_for_switch_groups(self, event_name_path):
        for switch_group_name in os.listdir(event_name_path):
            switch_group_path = os.path.join(event_name_path, switch_group_name)
            if os.path.isdir(switch_group_path):
                print('Found switch group ' + switch_group_name)
                print('Adding switch group name to dict if doesn\'t already exist...')
                self.switch_dict.setdefault(switch_group_name, set())
                self.search_for_switches(switch_group_name, switch_group_path)
                

    def search_for_events(self, event_name):
        event_name_path = os.path.join(self.main_folder_path, event_name)
        if os.path.isdir(event_name_path):
            print('Found event folder: ' + event_name)
            self.search_for_switch_groups(event_name_path)

def search_folder_for_switches_and_events(main_folder_path):
    result = FolderSearcher(main_folder_path)
    return result.switch_dict, result.event_dict
            
               