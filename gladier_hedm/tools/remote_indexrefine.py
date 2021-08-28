from gladier import GladierBaseTool, generate_flow_definition

def remote_indexrefine_args_builder(**data):
	return [{
		'endpoint':data.get('funcx_endpoint_compute','endpoint-not-found!'),
		'function':data.get('remote_indexrefine_funcx_id','function-id-not-found'),
		'payload': payload,
	} for payload in data.get('multipletasks',[])]

def remote_indexrefine(**event): # startLayerNr endLayerNr numProcs numBlocks blockNr timePath FileStem SeedFolder
	import os, subprocess
	startLayerNr = int(event.get('startLayerNr'))
	endLayerNr = int(event.get('endLayerNr'))
	numProcs = int(event.get('numProcs'))
	numBlocks = int(event.get('numBlocks'))
	blockNr = int(event.get('blockNr'))
	time_path = event.get('timePath')
	fStem = event.get('FileStem')
	topdir = event.get('SeedFolder')
	for layerNr in range(startLayerNr,endLayerNr+1):
		folderName = fStem + '_Layer_' + str(layerNr).zfill(4) + '_Analysis_Time_' + time_path
		thisDir = topdir + '/' + folderName + '/'
		os.chdir(thisDir)
		nSpotsToIndex = len(open('SpotsToIndex.csv').readlines())
		subprocess.call(os.path.expanduser("~/opt/MIDAS/FF_HEDM/bin/IndexerOMP")+' paramstest.txt '+str(blockNr)+' '+str(numBlocks)+' '+str(nSpotsToIndex)+' '+str(numProcs),shell=True)
		subprocess.call(os.path.expanduser("~/opt/MIDAS/FF_HEDM/bin/FitPosOrStrainsOMP")+' paramstest.txt '+str(blockNr)+' '+str(numBlocks)+' '+str(nSpotsToIndex)+' '+str(numProcs),shell=True)
	return 'done'

@generate_flow_definition(modifiers={
    remote_indexrefine: {'WaitTime': 7200,
		# ~ }
		'tasks':'$.RemoteIndexrefineArgsBuilder.details.result[0]',}
})
class RemoteIndexrefine(GladierBaseTool):
    funcx_functions = [
		remote_indexrefine_args_builder,
        remote_indexrefine
    ]
    required_input = [
		'multipletasks',
		# ~ 'startLayerNr',
		# ~ 'endLayerNr',
		# ~ 'numProcs',
		# ~ 'numBlocks',
		# ~ 'timePath',
		# ~ 'FileStem',
		# ~ 'SeedFolder',
		# ~ 'remote_indexrefine_funcx_id',
		'funcx_endpoint_compute',
    ]
