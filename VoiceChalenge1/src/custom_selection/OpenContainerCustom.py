'''
Created on Aug 25, 2016

@author: Flavio Ferreira
'''
from vocollect_core import obj_factory
from selection.OpenContainer import OpenContainer

from vocollect_core.dialog.functions import prompt_alpha_numeric , prompt_only
from vocollect_core import itext
from selection.SharedConstants import OPEN_CONTAINER_OPEN


import time

##############################################################################
class OpenContainer_Custom(OpenContainer):

    #----------------------------------------------------------
    def open_container(self):
        container=''
        
        if self._position == '':
            prompt = itext('selection.new.container.prompt.for.container.id')
           
        if self._region['promptForContainer'] == 1:
            result = prompt_alpha_numeric(prompt, 
                                          itext('selection.new.container.prompt.for.container.help'), 
                                          confirm=True,scan=True)
            container = result[0]
            
        result = -1
        if self._picks[0]['targetContainer'] == 0:
            target_container = ''
        else:
            target_container = self._picks[0]['targetContainer']
            
        while result < 0:
            result = self._container_lut.do_transmit(self._assignment['groupID'], 
                                                     self._assignment['assignmentID'], target_container, '', container, 2 , '')
        
        if result > 0:
            self.next_state = OPEN_CONTAINER_OPEN
            
        if result == 0:
            result = prompt_alpha_numeric(itext('voice.chalenge.badge'), 
                                          itext('voice.chalenge.badge'), 
                                          confirm=False,scan=True)

            prompt_only(itext('voice.chalenge.wait'))
            time.sleep(5) # delays for 10 seconds
            prompt_only(itext('voice.chalenge.mark'))
            time.sleep(3) 
            prompt_only(itext('voice.chalenge.get.set'))
            time.sleep(3) 
            prompt_only(itext('voice.chalenge.go'))



obj_factory.set_override(OpenContainer, OpenContainer_Custom)
