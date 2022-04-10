# DEVICEDUMP
#
# Ableton Live MIDI Remote Script to dump device parameter information
#
# Author: Jaap-henk Hoepman (info@xot.nl)
#
# Distributed under the MIT License, see LICENSE
#

# Python imorts
import os,sys

# Ableton Live imports
from _Framework.ControlSurface import ControlSurface

# set this to a local direcotory in your home
LOCALDIR = 'src/ableton-control-scripts/DEVICEDUMP/dumps'

def parameterdescription(p):
    l =     [f'{p.name} ({ p.original_name }):\n']
    l = l + [f'  Min: { p.str_for_value(p.min) } ({ p.min })\n']
    l = l + [f'  Cur: { p.str_for_value(p.value) } ({ p.value })\n']
    l = l + [f'  Max: { p.str_for_value(p.max) } ({ p.max })\n']
    if p.is_quantized:
        l = l + ['  Possible values: ']
        l = l + [', '.join(p.value_items)]                                    # join the possible value strings into one stirng, separated by a '
        l = l + ['\n']
    return ''.join(l)

class DEVICEDUMP(ControlSurface):
    u""" Script to dump the parameters of the currently selected device """

    def __init__(self, *a, **k):
        super(DEVICEDUMP, self).__init__(*a, **k)
        self._appointed_device = None
        self.log_message('DEVICEDUMP loaded.')
        self.log_message(f'My python version { sys.version }.')        

    def update_display(self):
        device = self.song().appointed_device
        if device != self._appointed_device:
            self._appointed_device = device
            name = device.class_name 
            home = os.path.expanduser("~")                                            # get home directory in device independent way: https://stackoverflow.com/questions/4028904/what-is-the-correct-cross-platform-way-to-get-the-home-directory-in-python
            path =  f'{ home }/{ LOCALDIR }'
            if not os.path.exists(path):
                path = home
            self.log_message(f'dumping device: { name }.')
            fname = f'{ path }/{ name }.dump'
            with open(fname,'w') as f:            
                parameters = device.parameters
                for p in parameters:
                    s = parameterdescription(p)
                    f.write(s)
            fname = f'{ path }/{ name }.parameternames'
            with open(fname,'w') as f:            
                parameters = device.parameters
                for p in parameters:
                    f.write(f"'{ p.original_name }',\n")

