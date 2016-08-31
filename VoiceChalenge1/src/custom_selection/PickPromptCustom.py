'''
Created on Aug 30, 2016

@author: Flavio Ferreira
'''
from selection.PickPrompt import PickPromptTask



from vocollect_core.dialog.functions import prompt_yes_no, prompt_only 

from vocollect_core import itext, obj_factory
#from .VarWeightsAndSerialNum import WeightsSerialNumbers
from selection.SharedConstants import SLOT_VERIFICATION, LOT_TRACKING

class PickPromptTask_Custom(PickPromptTask):
    '''Pick prompts base task
    Known implementations PickPromptMultipleTask, PickPromptSingleTask
    
     Steps:
            1. Check target containers
            2. Slot verification
            3. Case Label Check Digits
            4. Enter Quantity
            5. Quantity Verification
            6. Lot Tracking
            7. Initialize put records
            8. Put Prompt
            9. Weights and serial numbers
            10. Transmit picks
            11. Check for partial (should container be close and opened)
            12. Check close target container
            13. Check if done or where to return to in pick prompt
            14. Cycle count if needed
          
     Parameters
            region - region operator is picking in 
            assignment_lut - assignments currently working on
            picks - pick list for specific location
            container_lut - current list of containers
            taskRunner (Default = None) - Task runner object
            callingTask (Default = None) - Calling task (should be a pick prompt task)
    '''
    
    #------------------------------------------------------------
    def _verify_product_slot(self, result, is_scanned):
        '''Verifies product/slot depending on spoken check digit or spoken/scanned pvid or ready spoken'''
        #if ready is spoken and check digits is not blank prompt for check digit
        if result == 'ready' and self._picks[0]["checkDigits"] != '':
            prompt_only(itext('selection.pick.prompt.speak.check.digit'), True)
            self.next_state = SLOT_VERIFICATION
        #if pvid is scanned verify it matches the scanned product id
        elif is_scanned:
            if self._picks[0]["scannedProdID"] != result:
                prompt_only(itext('generic.wrongValue.prompt', result))
                self.next_state = SLOT_VERIFICATION
        #if check digit is spoken and both pvid and check digits are same prompt for identical short product
        elif result == self._picks[0]["checkDigits"] and self._pvid == result:
            if prompt_yes_no(itext('selection.pick.prompt.identical.product.short.product')):
                self._set_short_product(0)
                self.next_state = LOT_TRACKING
        #if ready or check digits  is spoken  and pvid is not blank prompt for short product
        elif result in [self._picks[0]["checkDigits"], 'ready'] and (self._pvid != '' or self._picks[0]["scannedProdID"] != ''):
            if prompt_yes_no(itext("selection.pick.prompt.short.product")):
                self._set_short_product(0)
                self.next_state = LOT_TRACKING
            else:
                prompt_only(itext('selection.pick.prompt.wrong.pvid'))
                self.next_state = SLOT_VERIFICATION





#Replace main class objects with new custom ones
obj_factory.set_override(PickPromptTask, PickPromptTask_Custom)
