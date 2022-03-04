from gladier import GladierBaseTool, generate_flow_definition

def remote_transforms(**data): # startLayerNr endLayerNr timePath FileStem SeedFolder paramFileName
	import os, subprocess
	startLayerNr = int(data.get('startLayerNr'))
	endLayerNr = int(data.get('endLayerNr'))
	time_path = data.get('timePath')
	fStem = data.get('FileStem')
	topdir = data.get('SeedFolder')
	paramFN = data.get('paramFileName')
	baseNameParamFN = paramFN.split('/')[-1]
	for layerNr in range(startLayerNr,endLayerNr+1):
		folderName = fStem + '_Layer_' + str(layerNr).zfill(4) + '_Analysis_Time_' + time_path
		thisDir = topdir + '/' + folderName + '/'
		os.chdir(thisDir)
		subprocess.call(os.path.expanduser("~/opt/MIDAS/FF_HEDM/bin/MergeOverlappingPeaksAll")+' '+baseNameParamFN,shell=True)
		subprocess.call(os.path.expanduser("~/opt/MIDAS/FF_HEDM/bin/CalcRadiusAll")+' '+baseNameParamFN,shell=True)
		subprocess.call(os.path.expanduser("~/opt/MIDAS/FF_HEDM/bin/FitSetup")+' '+baseNameParamFN,shell=True)
		subprocess.call(os.path.expanduser("~/opt/MIDAS/FF_HEDM/bin/SaveBinData"),shell=True)
	return 'done'

@generate_flow_definition(modifiers={
    remote_transforms: {'WaitTime': 7200}
})
class RemoteTransforms(GladierBaseTool):

    required_input = [
        'paramFileName',
        'startLayerNr',
        'endLayerNr',
        'timePath',
        'FileStem',
        'SeedFolder',
        'funcx_endpoint_compute',
    ]

    funcx_functions = [
        remote_transforms
    ]
