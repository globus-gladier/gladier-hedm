from gladier import GladierBaseTool, generate_flow_definition

def nf_remote_imageprocessing_args_builder(**data):
	return [{
		'endpoint':data.get('compute_endpoint','endpoint-not-found!'),
		'function':data.get('nf_remote_imageprocessing_compute_id','function-id-not-found'),
		'payload': payload,
	} for payload in data.get('multipletasks',[])]

def nf_remote_imageprocessing(**data): # startLayerNr endLayerNr numProcs numBlocks blockNr timePath FileStem SeedFolder
	import os, shutil, subprocess
	# ImageProcessing for each layer
	topParamFile = data.get('paramFile')
	OrigFileName = data.get('OrigFileName')
	startLayerNr = int(data.get('startLayerNr'))
	endLayerNr = int(data.get('endLayerNr'))
	nCPUs = data.get('numProcs')
	blockNr = data.get('blockNr')
	nBlocks = data.get('numBlocks')
	TopDataDirectory = data.get('TopDataDirectory')
	PFStem = '.'.join(topParamFile.split('.')[:-1])
	subFolder = TopDataDirectory+'/Analysis/nf/'
	Folder = OrigFileName.split('/')[-2]
	for layerNr in range(startLayerNr,endLayerNr+1):
		newFolder = subFolder+'/'+Folder+'_Layer_'+str(layerNr)+'/'
		os.chdir(newFolder)
		thisParamFile = PFStem + '_Layer_' + str(layerNr) + '.txt'
		subprocess.call(os.path.expanduser('~/opt/MIDAS/NF_HEDM/bin/ImageProcessingLibTiffOMP')+' '+thisParamFile+' '+str(blockNr)+' '+str(nBlocks)+' '+str(nCPUs),shell=True)
	return 'done'

@generate_flow_definition(modifiers={
    nf_remote_imageprocessing: {'WaitTime': 17200,
		'tasks':'$.NfRemoteImageprocessingArgsBuilder.details.result[0]',}
})
class NfRemoteImageProcessing(GladierBaseTool):
    compute_functions = [
		nf_remote_imageprocessing_args_builder,
        nf_remote_imageprocessing
    ]
    required_input = [
		'multipletasks',
		'compute_endpoint',
    ]
