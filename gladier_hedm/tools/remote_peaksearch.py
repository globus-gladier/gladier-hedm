from gladier import GladierBaseTool, generate_flow_definition

def remote_peaksearch_args_builder(**data):
	return [{
		'endpoint':data.get('compute_endpoint','endpoint-not-found!'),
		'function':data.get('remote_peaksearch_funcx_id','function-id-not-found'),
		'payload': payload,
	} for payload in data.get('multipletasks',[])]

def remote_peaksearch(**data): # startLayerNr endLayerNr nFrames numProcs numBlocks blockNr timePath FileStem SeedFolder paramFileName
	import os, subprocess, shutil
	startLayerNr = int(data.get('startLayerNr'))
	endLayerNr = int(data.get('endLayerNr'))
	nFrames = int(data.get('nFrames'))
	numProcs = int(data.get('numProcs'))
	numBlocks = int(data.get('numBlocks'))
	blockNr = int(data.get('blockNr'))
	time_path = data.get('timePath')
	fStem = data.get('FileStem')
	topdir = data.get('SeedFolder')
	paramFN = data.get('paramFileName')
	baseNameParamFN = paramFN.split('/')[-1]
	for layerNr in range(startLayerNr,endLayerNr+1):
		folderName = fStem + '_Layer_' + str(layerNr).zfill(4) + '_Analysis_Time_' + time_path
		thisDir = topdir + '/' + folderName + '/'
		os.chdir(thisDir)
		subprocess.call(os.path.expanduser("~/opt/MIDAS/FF_HEDM/bin/PeaksFittingOMP")+' '+
				baseNameParamFN+' '+ str(blockNr) + ' ' + str(numBlocks) + ' '+str(nFrames)+' '+str(numProcs),shell=True)
	return 'done'

@generate_flow_definition(modifiers={
    remote_peaksearch: {'WaitTime': 17200,
		'tasks':'$.RemotePeaksearchArgsBuilder.details.result[0]'}
})
class RemotePeaksearch(GladierBaseTool):
    compute_functions = [
		remote_peaksearch_args_builder,
        remote_peaksearch,
    ]
    required_input = [
		'multipletasks',
        'compute_endpoint',
    ]

