'''
Created on Aug 25, 2016

@author: Flavio Ferreira
'''
from vocollect_core import obj_factory
from selection.SelectionTask import SelectionTask

from vocollect_core import itext
from vocollect_core.dialog.functions import prompt_only
from core.SharedConstants import CORE_TASK_NAME, REQUEST_FUNCTIONS
from selection.SharedConstants import  GET_ASSIGNMENT
from selection.SelectionLuts import IN_PROGRESS_ANOTHER_FUNCTION, IN_PROGRESS_SPECIFIC_REGION
import time



##############################################################################
class SelectionTask_Custom(SelectionTask):
    #------------------------------------------------------------------------
    def validate_regions(self):
        ''' Validates a valid regions was received '''
        #check for valid regions, and that error code 3 
        #was not returned in either LUT
        self.set_sign_off_allowed(True)
        valid = False
        error_code = 0
        for region in self._valid_regions_lut:
            if region['errorCode'] == IN_PROGRESS_ANOTHER_FUNCTION:
                error_code = IN_PROGRESS_ANOTHER_FUNCTION
            if region['number'] >= 0:
                valid = True
        
        if valid and error_code == 0:
            for region in self._region_config_lut:
                if region['errorCode'] == IN_PROGRESS_ANOTHER_FUNCTION:
                    error_code = IN_PROGRESS_ANOTHER_FUNCTION

        #check if valid or not
        if error_code == IN_PROGRESS_ANOTHER_FUNCTION:
            self.return_to(CORE_TASK_NAME, REQUEST_FUNCTIONS)
        elif not valid:
            self.next_state = ''
            prompt_only(itext('generic.regionNotAuth.prompt'))
        else:
            self._region_selected = True
            if self._valid_regions_lut[0]['errorCode'] == IN_PROGRESS_SPECIFIC_REGION:
                self._inprogress_work = True
                prompt_only(itext('selection.getting.in-progress.work'))
            else:
                is_auto_issaunce = self._region_config_lut[0]['autoAssign'] == '1'
                max_work_ids = self._region_config_lut[0]['maxNumberWordID']
# FF _ don't say or ask anything, user cannot talk 
#                if (is_auto_issaunce and max_work_ids == 1):
#                    result = prompt_ready(itext('selection.start.picking'), False,
#                                                 {'change function' : False,
#                                                  'change region' : False}) 


    #----------------------------------------------------------
    def prompt_assignment_complete(self):
        # Successful LUT transmission, prompt for next assignment
# FF _ don't say or ask anything, user cannot talk 
#        result = prompt_ready(itext(self._assignment_complete_prompt_key), True,
#                              {'change function' : False,
#                               'change region' : False}) 

            self.next_state = GET_ASSIGNMENT
            # press pause
            time.sleep(1) 
            prompt_only(itext('voice.chalenge.press.pause'))
            time.sleep(5) 


    #----------------------------------------------------------
    def pick_assignment(self):
# ASk to scan his badge just to start the process
#        result = prompt_alpha_numeric(itext('voice.chalenge.badge'), 
#                                      itext('voice.chalenge.badge'), 
#                                      confirm=True,scan=True)
#        time.sleep(10) # delays for 10 seconds
#        prompt_only(itext('voice.chalenge.mark'))
#        time.sleep(3) 
#        prompt_only(itext('voice.chalenge.get.set'))
#        time.sleep(3) 
#        prompt_only(itext('voice.chalenge.go'))
 
        ''' perform pick assignment'''
        self._assignment_iterator = None
        self._pick_assignment_task.configure(self._current_region_rec,
                                             self._assignment_lut,
                                             self._picks_lut,
                                             self._container_lut,
                                             self.pick_only)
        self.launch(self._pick_assignment_task)
        



#Replace main class objects with new custom ones
obj_factory.set_override(SelectionTask, SelectionTask_Custom)
