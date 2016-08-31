'''
Created on Aug 30, 2016

@author: Flavio Ferreira
'''
from vocollect_core import obj_factory
from selection.PickPromptSingle import PickPromptSingleTask


from vocollect_core.dialog.functions import prompt_digits_required , prompt_only

from vocollect_core import itext
from selection.PickPrompt import SLOT_VERIFICATION
import vocollect_core.scanning as scanning


#----------------------------------------------------------
#Single pick prompt task
#----------------------------------------------------------
class PickPromptSingleTask_Custom(PickPromptSingleTask):
    '''Pick prompts for regions with single pick prompt defined
     Extends PickPromptTask
     
     Steps:
            1. Slot verification (Overridden)
            2. Enter Quantity (Overridden)
            
            Remaining steps are the same as base
          
     Parameters
             Same as base class
    '''
    
    #----------------------------------------------------------
    def slot_verification(self):
        '''override for Single Prompts''' 


        # turn scanner on
        scanning.set_scan_mode(scanning.ScanMode.Single, auto_trigger=True)
        # set time out for the scanner
        scanning.set_trigger_timeout(10)


#        prompt_only(itext('voice.chalenge.wait'))


        
        #if pick prompt type is 1 prompt only slot assuming they are picking just 1
        additional_vocabulary={'short product' : False, 
                               'ready' : False, 
                               'skip slot' : False,
                               'partial' : False}
      
        if self._region['pickPromptType'] == '1' and self._expected_quantity == 1:
            prompt = itext("selection.pick.prompt.single.slot.only", 
                                self._picks[0]["slot"],
                                self._uom, self._description, self._id_description, self._message)
        else:
            prompt = itext("selection.pick.prompt.single.pick.quantity", 
                                self._picks[0]["slot"],
                                self._expected_quantity, self._uom,  self._description, self._id_description, self._message)
   
        result, is_scanned = prompt_digits_required(prompt,
                                                    itext("selection.pick.prompt.checkdigit.help"), 
                                                    [self._picks[0]["checkDigits"], self._pvid], 
                                                    [self._picks[0]["scannedProdID"]], 
                                                    additional_vocabulary,
                                                    self._skip_prompt)
      
        self._skip_prompt = False
        if result == 'short product':
            self.next_state = SLOT_VERIFICATION
            self._validate_short_product()
            prompt_only(itext('selection.pick.prompt.check.digit'), True)
            self._skip_prompt = True #don't repeat main prompt
                
        elif result == 'partial':
            self.next_state = SLOT_VERIFICATION
            self._validate_partial(self._expected_quantity)
            prompt_only(itext('selection.pick.prompt.check.digit'), True)
            self._skip_prompt = True #don't repeat main prompt

        elif result == 'skip slot':
            self.next_state = SLOT_VERIFICATION
            self._skip_slot()
        else:
            self._verify_product_slot(result, is_scanned)
            
        # turn scanner off
        scanning.set_scan_mode(scanning.ScanMode.Single, auto_trigger=False)




#Replace main class objects with new custom ones
obj_factory.set_override(PickPromptSingleTask, PickPromptSingleTask_Custom)
