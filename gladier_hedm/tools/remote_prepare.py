from gladier import GladierBaseTool, generate_flow_definition

def remote_prepare(**event):  #paramFileName startLayerNr endLayerNr timePath StartFileNrFirstLayer NrFilesPerSweep FileStem SeedFolder StartNr EndNr
	import numpy as np
	import os, subprocess
	import datetime
	from pathlib import Path
	import shutil
	
	paramFN = event.get('paramFileName')
	startLayerNr = int(event.get('startLayerNr'))
	endLayerNr = int(event.get('endLayerNr'))
	time_path = event.get('timePath')
	startFileNrFirstLayer = int(event.get('StartFileNrFirstLayer'))
	nrFilesPerSweep = int(event.get('NrFilesPerSweep'))
	fStem = event.get('FileStem')
	topdir = event.get('SeedFolder')
	startNr = int(event.get('StartNr'))
	endNr = int(event.get('EndNr'))
	darkFN = even.get('darkFN')
	paramContents = open(paramFN).readlines()
	os.chdir(topdir)
	baseNameParamFN = paramFN.split('/')[-1]
	homedir = os.path.expanduser('~')
	nFrames = endNr - startNr + 1
	for layerNr in range(startLayerNr,endLayerNr+1):
		thisStartNr = startNrFirstLayer + (layerNr-1)*nrFilesPerSweep
		folderName = fStem + '_Layer_' + str(layerNr).zfill(4) + '_Analysis_Time_' + time_path
		thisDir = topdir + '/' + folderName + '/'
		Path(thisDir).mkdir(parents=True,exist_ok=True)
		os.chdir(thisDir)
		thisParamFN = thisDir + baseNameParamFN
		thisPF = open(thisParamFN,'w')
		for line in paramContents:
			thisPF.write(line)
		thisPF.write('RawFolder '+topdir+'\n')
		thisPF.write('SeedFolder '+topdir+'\n')
		thisPF.write('Dark '+topdir+'/'+darkFN+'\n')
		thisPF.write('Folder '+thisDir+'\n')
		thisPF.write('LayerNr '+str(layerNr)+'\n')
		thisPF.write('StartFileNr '+str(thisStartNr)+'\n')
		thisPF.close()
		Path(thisDir+'/Temp').mkdir(parents=True,exist_ok=True)
		Path(thisDir+'Output').mkdir(parents=True,exist_ok=True)
		Path(thisDir+'Results').mkdir(parents=True,exist_ok=True)
		subprocess.call(os.path.expanduser("~/opt/MIDAS/FF_HEDM/bin/GetHKLList")+" "+thisParamFN,shell=True)

@generate_flow_definition(modifiers={
    remote_prepare: {'WaitTime': 7200}
})
class RemotePrepare(GladierBaseTool):

    required_input = [
        'paramFileName',
        'startLayerNr',
        'endLayerNr',
        'timePath',
        'StartFileNrFirstLayer',
        'NrFilesPerSweep',
        'FileStem',
        'SeedFolder',
        'darkFN',
        'StartNr',
        'EndNr',
        'funcx_endpoint_compute',
    ]

    funcx_functions = [
        remote_prepare
    ]
