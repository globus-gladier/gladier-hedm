from gladier import GladierBaseTool, generate_flow_definition

def nf_remote_fitorientation_args_builder(**data):
	return [{
		'endpoint':data.get('funcx_endpoint_compute','endpoint-not-found!'),
		'function':data.get('nf_remote_fitorientation_funcx_id','function-id-not-found'),
		'payload': payload,
	} for payload in data.get('multipletasks',[])]

def nf_remote_fitorientation(**data): # startLayerNr endLayerNr numProcs numBlocks blockNr timePath FileStem SeedFolder
	import os, shutil, subprocess
	warnings.filterwarnings('ignore')
	# FitOrientation for each layer
	topParamFile = data.get('paramFile')
	OrigFileName = data.get('OrigFileName')
	startLayerNr = int(data.get('startLayerNr'))
	endLayerNr = int(data.get('endLayerNr'))
	nCPUs = data.get('numProcs')
	blockNr = data.get('blockNr')
	nBlocks = data.get('numBlocks')
	TopDataDirectory = data.get('TopDataDirectory')
	PFStem = '.'.join(topParamFile.split('.')[:-1])
	Folder = 'Analysis/' + '/'.join(OrigFileName.split('/')[:-1])
	for layerNr in range(startLayerNr,endLayerNr+1):
		newFolder = TopDataDirectory+'/'+Folder+'_Layer_'+str(layerNr)+'/'
		os.chdir(newFolder)
		thisParamFile = PFStem + '_Layer_' + str(layerNr) + '.txt'
		subprocess.call(os.path.expanduser('~/opt/MIDAS/NF_HEDM/bin/FitOrientationOMP')+' '+thisParamFile+' '+blockNr+' '+nBlocks+' '+nCPUs,shell=True)
	return 'done'

@generate_flow_definition(modifiers={
    nf_remote_fitorientation: {'WaitTime': 17200,
		'tasks':'$.NfRemoteFitOrientationArgsBuilder.details.result[0]',}
})
class NfRemoteFitOrientation(GladierBaseTool):
    funcx_functions = [
		nf_remote_fitorientation_args_builder,
        nf_remote_fitorientation
    ]
    required_input = [
		'multipletasks',
		'funcx_endpoint_compute',
    ]
