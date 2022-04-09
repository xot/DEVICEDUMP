# DEVICEDUMP

Ableton Live MIDI Remote Script to dump device parameter information.

Dumps two files in the user home directory, or in a sub-directory specified in the source:

<device.class_name>.dump
: dumping all parameter information (min, cur and max values as reproted by Ableton and as floats, and possibly the enumeration of all possible values the parameter can assume.

<device.class_name>.parameternames
: listing only the original parameter names, separated by commas

## Installation

Copy ```__init.py__``` and ```DEVICEDUMP.py``` to your local Ableton MIDI Live Scripts folder (```~/Music/Ableton/User Library/Remote Scripts/``` on MacOS and
```~\Documents\Ableton\User Library\Remote Scripts``` on Windows).

Edit the ```LOCALDIR``` constant in ```DEVICEDUMP.py``` to change the default location where dumps are saved.

Add DEVICEDUMP as a Control Surface in Live > Preferences > MIDI.

Any device selected (the 'Blue Hand') will automatically be dumped.

See ```~/Library/Preferences/Ableton/Live <version>/Log.txt``` for any error messages.
