# ImportSwitchesWaapi

A WAAPI script for automating the creation of Switch Groups and associated Switch Containers in Wwise.

## Functionality

This script is designed to take a folder path as input, and use the provided folder to create Switch Groups and associated Switch Containers in an open Wwise project.

The current expected input is the argument main_folder_path which is a path that should have the following kind of structure:

```
main_folder_path/
├── Sound_Event_1/
│ ├── Switch_Group_Name_1/
│ │ ├── Switch_Name_1/
│ │ ├── Switch_Name_2/
│ │ ├── Switch_Name_3.Switch_Name_4/
│ │ └── Switch_Name_5/
│ ├── Switch_Group_Name_2/
│ │ ├── Switch_Name_1/
│ │ ├── Switch_Name_2/
│ │ ├── Switch_Name_3/
│ │ ├── Switch_Name_4/
│ │ └── Switch_Name_5/
├── Sound_Event_2/
│ ├── Switch_Group_Name_1/
│ │ ├── Switch_Name_1/
│ │ ├── Switch_Name_2/
│ │ ├── Switch_Name_3/
│ │ ├── Switch_Name_4/
│ │ └── Switch_Name_5/
│ ├── Switch_Group_Name_2/
│ │ ├── Switch_Name_1/
│ │ ├── Switch_Name_2/
│ │ ├── Switch_Name_3/
│ │ ├── Switch_Name_4/
│ │ └── Switch_Name_5/
```

The script will take this file structure and identify the unique Switch Groups defined within it. It will then try to connect to an open Wwise project and create these Switch Groups if they do not already exist. It will also create the Switches within those groups if they do not already exist.

Note that the switch name folders can be given a single name, or multiple names joined by '.' this is so that once this script imports audio files as well you can show that you want a single folder of audio files to be associated with multiple Switches.
