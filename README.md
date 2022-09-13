# pyStation
### Info

A command line python script for managing mods for World of Warships, helpful for use on platforms not supported by ModStation such as Linux.

## Setup

### Download

Download the latest version from the Releases page. 

### Initial file setup

To avoid possible issues with distributing wargaming files you will need to manually copy the *.Configuration* file of ModStation into the folder of this script and rename it to *modlist.xml*:

This mod list can be copied from `C:\ProgramData\Wargaming.net\World of Warships ModStation\.Cache\0.11.8.0\.Configuration` replacing 0.11.8.0 with the latest game version. Rename the file to *modlist.xml*.

After this you can edit the *wowsModManager.txt* file to set your game folder path. This should be the main folder, e.g. `E:\Games\World_of_Warships_EU` on the E: drive of a Windows system.

## Usage

### help | man

Print a list of commands.

### install

Install a mod. After running *install* you'll be asked to enter a mod name, such as *FSI_Yamato*.

### uninstall

Uninstall a mod. After running *uninstall* you'll be asked to enter a mod name, such as *FSI_Yamato*. Currently this works by downloading the mod files again as what files a mod adds aren't cached. This isn't very efficient.

### downloadpatch

Download a patch file. After running *downloadpatch* you'll be asked to enter a mod name, such as *UI_RegenAssistant*. The patch is currently intended only for manual use, changes won't automatically be made.

### list

List mods. After running *list* you'll be asked for what types of mods to list, options being `all, crosshair, hudlib, shipicons, shipshell, ui, port, other`.

### listinstall

Install all mods in the *installed.txt* file. This is done by automatically running the *install* command for each mod.

### listuninstall

Uninstall all mods in the *installed.txt* file. This is done by automatically running the *uninstall* command for each mod.

### exit

Stop pyStation.

## Issues / Missing features

- Some mods come with "patches" which involve editing and copying existing game files, these aren't currently implemented and have to be done manually. A warning is given when dealing with a mod with a patch file. Patch files can be downloaded with *downloadpatch* if you wish to look at them or manually install them.