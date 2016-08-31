import mock_catalyst
from mock_catalyst import EndOfApplication
from vocollect_lut_odr_test.mock_server import MockServer, BOTH_SERVERS
from main import main

#create a simulated host server - using TEST1.XML
ms = MockServer(use_std_in_out = True)
ms = MockServer(use_std_in_out = True, lut_port=15008, odr_port=15009)
mock_catalyst.environment_properties['SwVersion.Locale']='pt_BR'
ms.start_server(BOTH_SERVERS)
ms.load_server_responses("Test/voicelink_test/Data/test1.xml")
ms.set_server_response('Y', 'prTaskODR')

#Post responses
mock_catalyst.post_dialog_responses('ready',
                                  '123!','3!','yes','1','yes')


#

#create a simulated host server - USING vl
#ms = MockServer(use_std_in_out = True, lut_port=15004, odr_port=15005)
#mock_catalyst.environment_properties['SwVersion.Locale']='pt_BR'
#ms.set_pass_through_host('192.168.2.101', 15004, 15005)
#ms.set_server_response('Y', 'prTaskODR')




try:
    main()
except EndOfApplication as err:
    print('Application ended')
    
ms.stop_server(BOTH_SERVERS)


#Sample test case creation
#from CreateTestFile import CreateTestFile
#test = CreateTestFile('Sample', ms)
#path = '' #should end with slash if specified (i.e. test\functional_tests\Selection_tests\)
#test.write_test_to_file(path)
