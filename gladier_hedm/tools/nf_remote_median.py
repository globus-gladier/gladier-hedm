from gladier import GladierBaseTool, generate_flow_definition

def nf_remote_median_args_builder(**data):
	return [{
		'endpoint':data.get('compute_endpoint','endpoint-not-found!'),
		'function':data.get('nf_remote_median_compute_id','function-id-not-found'),
		'payload': payload,
	} for payload in data.get('mediantasks',[])]

def nf_remote_median(**data): # startLayerNr endLayerNr numProcs numBlocks blockNr timePath FileStem SeedFolder
	import os, shutil, subprocess
	# Median for each layer
	topParamFile = data.get('paramFile')
	OrigFileName = data.get('OrigFileName')
	startLayerNr = int(data.get('startLayerNr'))
	endLayerNr = int(data.get('endLayerNr'))
	distanceNr = data.get('distanceNr')
	TopDataDirectory = data.get('TopDataDirectory')
	PFStem = '.'.join(topParamFile.split('.')[:-1])
	subFolder = TopDataDirectory+'/Analysis/nf/'
	Folder = OrigFileName.split('/')[-2]
	for layerNr in range(startLayerNr,endLayerNr+1):
		newFolder = subFolder+'/'+Folder+'_Layer_'+str(layerNr)+'/'
		os.chdir(newFolder)
		thisParamFile = PFStem + '_Layer_' + str(layerNr) + '.txt'
		subprocess.call(os.path.expanduser('~/opt/MIDAS/NF_HEDM/bin/MedianImageLibTiff')+' '+thisParamFile+' '+str(distanceNr),shell=True)
	return 'done'

@generate_flow_definition(modifiers={
    nf_remote_median: {'WaitTime': 17200,
		'tasks':'$.NfRemoteMedianArgsBuilder.details.result[0]',}
})
class NfRemoteMedian(GladierBaseTool):
    compute_functions = [
		nf_remote_median_args_builder,
        nf_remote_median
    ]
    required_input = [
		'mediantasks',
		'compute_endpoint',
    ]
