'''
Created on Aug 25, 2016

@author: Flavio Ferreira
'''

from selection.PickAssignment import PickAssignmentTask

from vocollect_core import obj_factory
from selection.SharedConstants import PICK_ASSIGNMENT_END_PICKING, PICK_ASSIGNMENT_CHECK_NEXT_PICK
from selection.PickPromptMultiple import PickPromptMultipleTask
from selection.PickPromptSingle import PickPromptSingleTask

import vocollect_core.scanning as scanning
import time


#===========================================================
#Pick Assignment Task
#===========================================================
class PickAssignmentTask_Custom(PickAssignmentTask):
    #----------------------------------------------------------
    def check_next_pick(self):
        ''' Checks next pick'''

        #check for next pick
        self._auto_short = False
        
        # Holds the complete next pick list at the end
        self._pickList = []
        
        # Holds the first pick found with the right status
        first_pick = None
        
        # Holds candidates for matching picks
        candidates = []
        
        if self._region['containerType'] == 0:
            combine_assignments = False
        else:
            combine_assignments = True
        
        # Search for a pick with the correct status. Process all picks in
        # the LUT, remembering possible match candidates.    
        for pick in self._picks_lut:
            if pick['status'] == self.status and first_pick == None:
                first_pick = pick;
                self._pickList.append(pick)
            elif pick['status'] != 'P':
                # This is a match candidate
                candidates.append(pick)

    
        if first_pick != None:               
            #Check for any matching picks among the candidates
            if len(candidates) > 0:
                for pick in candidates:
                    if self._picks_lut.picks_match(first_pick, pick, combine_assignments): 
                        self._pickList.append(pick)
                        pick['status'] = first_pick['status']

            self.dynamic_vocab.next_pick(self._pickList)   
            time.sleep(2) 

        else:
            #No more picks
            self.next_state = PICK_ASSIGNMENT_END_PICKING
        
    #----------------------------------------------------------        
    def pick_prompt(self):

        '''Pick prompt Multiple and single'''
        if self._pick_prompt_task is None:
            if(self._region['pickPromptType'] == '2'):
                self._pick_prompt_task = obj_factory.get(PickPromptMultipleTask,
                                              self._region,
                                              self._assignment_lut, 
                                              self._pickList,
                                              self._container_lut, 
                                              self._auto_short,
                                              self.taskRunner, self)
            else:
                self._pick_prompt_task = obj_factory.get(PickPromptSingleTask,
                                              self._region,
                                              self._assignment_lut, 
                                              self._pickList,
                                              self._container_lut, 
                                              self._auto_short,
                                              self.taskRunner, self)
        else:
            self._pick_prompt_task.config(self._pickList,
                                          self._auto_short)
        self.launch(self._pick_prompt_task,
                PICK_ASSIGNMENT_CHECK_NEXT_PICK)
     
    #----------------------------------------------------------        



#Replace main class objects with new custom ones
obj_factory.set_override(PickAssignmentTask, PickAssignmentTask_Custom)
