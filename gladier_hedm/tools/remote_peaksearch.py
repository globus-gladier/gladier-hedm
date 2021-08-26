from gladier import GladierBaseTool, generate_flow_definition

def remote_peaksearch(**event): # startLayerNr endLayerNr nFrames numProcs numBlocks blockNr timePath FileStem SeedFolder paramFileName
	import os, subprocess
	startLayerNr = int(event.get('startLayerNr'))
	endLayerNr = int(event.get('endLayerNr'))
	nFrames = int(event.get('nFrames'))
	numProcs = int(event.get('numProcs'))
	numBlocks = int(event.get('numBlocks'))
	blockNr = int(event.get('blockNr'))
	time_path = event.get('timePath')
	fStem = event.get('FileStem')
	topdir = event.get('SeedFolder')
	paramFN = event.get('paramFileName')
	baseNameParamFN = paramFN.split('/')[-1]
	for layerNr in range(startLayerNr,endLayerNr+1):
		folderName = fStem + '_Layer_' + str(layerNr).zfill(4) + '_Analysis_Time_' + time_path
		thisDir = topdir + '/' + folderName + '/'
		os.chdir(thisDir)
		subprocess.call(os.path.expanduser("~/opt/MIDAS/FF_HEDM/bin/PeaksFittingOMP")+' '+baseNameParamFN+' '+ blockNr + ' ' + numBlocks + ' '+str(nFrames)+' '+str(numProcs),shell=True)

@generate_flow_definition(modifiers={
    remote_peaksearch: {'WaitTime': 25000,
		'tasks':'$.input.peaksearch_tasks',}
})
class RemotePeaksearch(GladierBaseTool):
    funcx_functions = [
        remote_peaksearch
    ]
    required_input = [
		'remote_peaksearch_funcx_id',
        'funcx_endpoint_compute',
    ]

