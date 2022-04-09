# DEVICEDUMP
#
# Ableton Live MIDI Remote Script to dump device parameter information
#
# Author: Jaap-henk Hoepman (info@xot.nl)
#
# Distributed under the MIT License, see LICENSE
#

# Python imorts
import os 

# Ableton Live imports
from _Framework.ControlSurface import ControlSurface

# set this to a local direcotory in your home
LOCALDIR = 'src/ableton-control-scripts/DEVICEDUMP/dumps'

def parameterdescription(p):
    s = p.name + '(' + p.original_name + '):\n  '
    s = s + 'Min: ' + p.str_for_value(p.min) + ' (' + str(p.min) + ')\n  '
    s = s + 'Cur: ' + p.str_for_value(p.value) + ' (' + str(p.value) + ')\n  '
    s = s + 'Max: ' + p.str_for_value(p.max) + ' (' + str(p.max) + ')'
    if p.is_quantized:
        s = s + '\n  Possible values: '
        first = True
        for v in p.value_items:
            if not first:
                s = s + ", "
            first = False
            s = s + str(v) 
    s = s + '\n'
    return s

class DEVICEDUMP(ControlSurface):
    u""" Script to dump the parameters of the currently selected device """

    def __init__(self, *a, **k):
        super(DEVICEDUMP, self).__init__(*a, **k)
        self._appointed_device = None
        self.log_message("DEVICEDUMP loaded.")

    def update_display(self):
        device = self.song().appointed_device
        if device != self._appointed_device:
            self._appointed_device = device
            name = device.class_name 
            home = os.path.expanduser("~")                                            # get home directory in device independent way: https://stackoverflow.com/questions/4028904/what-is-the-correct-cross-platform-way-to-get-the-home-directory-in-python
            path =  home + '/' + LOCALDIR
            if os.path.exists(path):
                self.log_message("dumping device: " + name)
                fname = path + '/' + name + '.dump'
                with open(fname,'w') as f:            
                    parameters = device.parameters
                    for p in parameters:
                        s = parameterdescription(p)
                        f.write(s)
                fname = path + '/' + name + '.parameternames'
                with open(fname,'w') as f:            
                    parameters = device.parameters
                    for p in parameters:
                        s = "'" + p.original_name + "',\n"
                        f.write(s)
            else:
                self.log_message("path does not exist: " + path)                

