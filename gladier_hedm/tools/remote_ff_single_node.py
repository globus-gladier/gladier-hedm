from gladier import GladierBaseTool, generate_flow_definition

def remote_ff_single_node(**event):  #paramFileName startLayerNr endLayerNr timePath StartFileNrFirstLayer NrFilesPerSweep FileStem SeedFolder StartNr EndNr
	import numpy as np
	import os, subprocess
	import datetime
	from pathlib import Path
	import shutil

	paramFN = event.get('paramFileName')
	startLayerNr = int(event.get('startLayerNr'))
	endLayerNr = int(event.get('endLayerNr'))
	time_path = event.get('timePath')
	startNrFirstLayer = int(event.get('StartFileNrFirstLayer'))
	nrFilesPerSweep = int(event.get('NrFilesPerSweep'))
	fStem = event.get('FileStem')
	topdir = event.get('SeedFolder')
	startNr = int(event.get('StartNr'))
	endNr = int(event.get('EndNr'))
	darkFN = event.get('darkFN')
	nFrames = event.get('nFrames')
	numBlocks = event.get('numBlocks')
	numProcs = event.get('numProcs')
	blockNr = 0
	os.chdir(topdir)
	paramContents = open(paramFN).readlines()
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
		subprocess.call(os.path.expanduser("~/opt/MIDAS/FF_HEDM/bin/GetHKLList")+" "+baseNameParamFN,shell=True)
		subprocess.call(os.path.expanduser("~/opt/MIDAS/FF_HEDM/bin/PeaksFittingOMP")+' '+baseNameParamFN+' '+ str(blockNr) + ' ' + str(numBlocks) + ' '+str(nFrames)+' '+str(numProcs),shell=True)
		subprocess.call(os.path.expanduser("~/opt/MIDAS/FF_HEDM/bin/MergeOverlappingPeaksAll")+' '+baseNameParamFN,shell=True)
		subprocess.call(os.path.expanduser("~/opt/MIDAS/FF_HEDM/bin/CalcRadiusAll")+' '+baseNameParamFN,shell=True)
		subprocess.call(os.path.expanduser("~/opt/MIDAS/FF_HEDM/bin/FitSetup")+' '+baseNameParamFN,shell=True)
		subprocess.call(os.path.expanduser("~/opt/MIDAS/FF_HEDM/bin/SaveBinData"),shell=True)
		nSpotsToIndex = len(open('SpotsToIndex.csv').readlines())
		subprocess.call(os.path.expanduser("~/opt/MIDAS/FF_HEDM/bin/IndexerOMP")+' paramstest.txt '+str(blockNr)+' '+str(numBlocks)+' '+str(nSpotsToIndex)+' '+str(numProcs),shell=True)
		subprocess.call(os.path.expanduser("~/opt/MIDAS/FF_HEDM/bin/FitPosOrStrainsOMP")+' paramstest.txt '+str(blockNr)+' '+str(numBlocks)+' '+str(nSpotsToIndex)+' '+str(numProcs),shell=True)
		subprocess.call(os.path.expanduser('~/opt/MIDAS/FF_HEDM/bin/ProcessGrains') + ' ' + baseNameParamFN,shell=True)
		os.chdir(topdir)
	subprocess.call('tar -czf recon_'+time_path+'.tar.gz *_Analysis_Time_'+time_path+'*',shell=True)
	return 'done'

@generate_flow_definition(modifiers={
    remote_ff_single_node: {'WaitTime': 7200}
})
class RemoteFFSingleNode(GladierBaseTool):

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
        'nFrames',
        'StartNr',
        'EndNr',
        'numBlocks',
        'funcx_endpoint_compute',
    ]

    funcx_functions = [
        remote_ff_single_node
    ]
