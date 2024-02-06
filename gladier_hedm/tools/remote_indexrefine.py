from gladier import GladierBaseTool, generate_flow_definition

def remote_indexrefine_args_builder(**data):
	return [{
		'endpoint':data.get('compute_endpoint','endpoint-not-found!'),
		'function':data.get('remote_indexrefine_compute_id','function-id-not-found'),
		'payload': payload,
	} for payload in data.get('multipletasks',[])]

def remote_indexrefine(**data): # startLayerNr endLayerNr numProcs numBlocks blockNr timePath FileStem SeedFolder
	import os, subprocess
	startLayerNr = int(data.get('startLayerNr'))
	endLayerNr = int(data.get('endLayerNr'))
	numProcs = int(data.get('numProcs'))
	numBlocks = int(data.get('numBlocks'))
	blockNr = int(data.get('blockNr'))
	time_path = data.get('timePath')
	fStem = data.get('FileStem')
	topdir = data.get('SeedFolder')
	for layerNr in range(startLayerNr,endLayerNr+1):
		folderName = fStem + '_Layer_' + str(layerNr).zfill(4) + '_Analysis_Time_' + time_path
		thisDir = topdir + '/' + folderName + '/'
		os.chdir(thisDir)
		nSpotsToIndex = len(open('SpotsToIndex.csv').readlines())
		subprocess.call(os.path.expanduser("~/opt/MIDAS/FF_HEDM/bin/IndexerOMP")+' paramstest.txt '+str(blockNr)+' '+str(numBlocks)+' '+str(nSpotsToIndex)+' '+str(numProcs),shell=True)
		subprocess.call(os.path.expanduser("~/opt/MIDAS/FF_HEDM/bin/FitPosOrStrainsOMP")+' paramstest.txt '+str(blockNr)+' '+str(numBlocks)+' '+str(nSpotsToIndex)+' '+str(numProcs),shell=True)
		subprocess.call('touch tr.txt',shell=True)
	return 'done'

@generate_flow_definition(modifiers={
    remote_indexrefine: {'WaitTime': 17200,
		'tasks':'$.RemoteIndexrefineArgsBuilder.details.result[0]',}
})
class RemoteIndexrefine(GladierBaseTool):
    compute_functions = [
		remote_indexrefine_args_builder,
        remote_indexrefine
    ]
    required_input = [
		'multipletasks',
		'compute_endpoint',
    ]
