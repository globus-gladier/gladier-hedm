from gladier import GladierBaseTool, generate_flow_definition

def remote_find_grains(**event): # startLayerNr endLayerNr timePath FileStem SeedFolder paramFileName
	import os, subprocess
	startLayerNr = int(event.get('startLayerNr'))
	endLayerNr = int(event.get('endLayerNr'))
	time_path = event.get('timePath')
	fStem = event.get('FileStem')
	topdir = event.get('SeedFolder')
	paramFN = event.get('paramFileName')
	baseNameParamFN = paramFN.split('/')[-1]
	for layerNr in range(startLayerNr,endLayerNr+1):
		folderName = fStem + '_Layer_' + str(layerNr).zfill(4) + '_Analysis_Time_' + time_path
		thisDir = topdir + '/' + folderName + '/'
		os.chdir(thisDir)
		subprocess.call(os.path.expanduser('~/opt/MIDAS/FF_HEDM/bin/ProcessGrains') + ' ' + baseNameParamFN,shell=True)
		os.chdir(topdir)
	subprocess.call('tar -czf recon_'+time_path+'.tar.gz *_Analysis_Time_'+time_path+'*',shell=True)




@generate_flow_definition(modifiers={
    remote_find_grains: {'WaitTime': 7200},
    
})
class RemoteFindGrains(GladierBaseTool):

    required_input = [
        'paramFileName',
        'startLayerNr',
        'endLayerNr',
        'timePath',
        'FileStem',
        'SeedFolder',
        'flags',
        'funcx_endpoint_compute',
    ]

    funcx_functions = [
        remote_find_grains
    ]
