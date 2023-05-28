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
import Live
from Live.Browser import *

# set this to a local direcotory in your home
LOCALDIR = 'src/ableton-control-scripts/DEVICEDUMP/dumps'

DEBUG = 1

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
        self.idx = 1
        self.dumpall = True 
        self.log_message('DEVICEDUMP loaded.')
        self.log_message(f'My python version { sys.version }.')        

    def debug(self, level, m):
        """Write a debug message to the log, if level < DEBUG.
        """
        if level <= DEBUG:
            self.log_message(f'E1 (debug): {m}')

    def dump_device(self,device):
        classname = device.class_name 
        name = device.name
        home = os.path.expanduser("~")                                            # get home directory in device independent way: https://stackoverflow.com/questions/4028904/what-is-the-correct-cross-platform-way-to-get-the-home-directory-in-python
        path =  f'{ home }/{ LOCALDIR }'
        if not os.path.exists(path):
            path = home
        self.debug(1,f'dumping device: { classname } (aka {name}).')
        fname = f'{ path }/{ classname }={ name }.dump'
        with open(fname,'w') as f:            
            parameters = device.parameters
            for p in parameters:
                s = parameterdescription(p)
                f.write(s)
        fname = f'{ path }/{ classname }={ name }.parameternames'
        with open(fname,'w') as f:            
            parameters = device.parameters
            for p in parameters:
                f.write(f"'{ p.original_name }',\n")        
        
    def dump_when_changed(self):
        device = self.song().appointed_device
        self.debug(2,f'Appointed device {device}')
        if device and device != self._appointed_device:
            self._appointed_device = device
            self.dump_device(device)
        if device and device == self._appointed_device:
            self.debug(2,f'Appointed device not changed.')
        else:
            self.debug(2,f'No appointed device.')

    def dump_browser_item(self,browser,item):
        self.debug(1,f'Item {item.name}')
        if item.is_device:
            track = self.song().view.selected_track
            browser.load_item(item)
            itemidx = len(track.devices)-1
            device = track.devices[itemidx]
            self.dump_device(device)
            self.debug(1,f'Track device {device.name}')
            track.delete_device(itemidx)
        for child in item.children:
            self.dump_browser_item(browser,child)

    def dump_all(self):
        application = Live.Application.get_application()
        browser = application.browser
        for child in browser.midi_effects.children:
            self.dump_browser_item(browser,child)
        for child in browser.audio_effects.children:
            self.dump_browser_item(browser,child)
        for child in browser.instruments.children:
            self.dump_browser_item(browser,child)
        
    def update_display(self):
        if self.dumpall:
            self.dump_all()
        self.dumpall = False
        #self.dump_when_changed()
            
    def build_midi_map(self, midi_map_handle):
        self.debug(1,f'Building MIDI map {self.idx}')
        self.idx += 1

    def refresh_state(self):
        self.debug(1,f'Refreshing state {self.idx}')
        self.idx += 1
        
