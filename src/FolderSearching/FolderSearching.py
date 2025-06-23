import os

class FolderSearcher:
    def __init__(self, main_folder_path):
        self.main_folder_path = main_folder_path
        self.switch_dict = {} # a dict of switchGroupName -> switchName[] for creating switches
        self.event_dict = {} # a dict of event_name -> dict(switchGroupName -> dict(switchName -> set(audioFilePath, audioFilePath2...)))

        if os.path.exists(self.main_folder_path) & os.path.isdir(self.main_folder_path):
            print('Searching location: ' + main_folder_path + ' for switches and events...')
            for event_name in os.listdir(main_folder_path):
                self.search_for_events(event_name)

            print(f"\n### Switches have been searched, found {self.switch_dict} ###\n")
            print(f"\n### Events have been searched, found {self.event_dict} ###\n")
        else:
            print(f"\nERROR: Location {main_folder_path} not found.\n")

    def search_for_audio_files(self, event_name, switch_group_name, switch_name_list, switch_path):
        print(f"Searching for audio files associated with switch(es): {switch_name_list}")
        for audio_file in os.listdir(switch_path):
            audio_file_path = os.path.join(switch_path, audio_file)
            if os.path.isfile(audio_file_path):
                for switch_name in switch_name_list:
                    self.event_dict[event_name][switch_group_name][switch_name].add(audio_file_path) # save full path to make import easier later

    def search_for_switches(self, event_name, switch_group_name, switch_group_path):
        for switch_name_list in os.listdir(switch_group_path):
            switch_path = os.path.join(switch_group_path, switch_name_list)
            if os.path.isdir(switch_path):
                switch_name_list = switch_name_list.split(',')
                for switch_name in switch_name_list:    
                    print('Found switch: ' + switch_name + ' adding to switch group...')
                    self.event_dict[event_name][switch_group_name].setdefault(switch_name, set())
                    self.switch_dict[switch_group_name].add(switch_name)
                self.search_for_audio_files(event_name, switch_group_name, switch_name_list, switch_path)


    def search_for_switch_groups(self, event_name, event_name_path):
        for switch_group_name in os.listdir(event_name_path):
            switch_group_path = os.path.join(event_name_path, switch_group_name)
            if os.path.isdir(switch_group_path):
                print('Found switch group ' + switch_group_name)
                print('Adding switch group name to dict if doesn\'t already exist...')
                self.event_dict[event_name].setdefault(switch_group_name, {})
                self.switch_dict.setdefault(switch_group_name, set())
                self.search_for_switches(event_name, switch_group_name, switch_group_path)
                

    def search_for_events(self, event_name):
        event_name_path = os.path.join(self.main_folder_path, event_name)
        if os.path.isdir(event_name_path):
            print('Found event folder: ' + event_name)
            self.event_dict.setdefault(event_name, {})
            self.search_for_switch_groups(event_name, event_name_path)

def search_folder_for_switches_and_events(main_folder_path):
    result = FolderSearcher(main_folder_path)
    return result.switch_dict, result.event_dict
