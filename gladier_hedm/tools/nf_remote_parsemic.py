from gladier import GladierBaseTool, generate_flow_definition

def nf_remote_parsemic(**data):  #paramFileName startLayerNr endLayerNr timePath StartFileNrFirstLayer NrFilesPerSweep FileStem SeedFolder StartNr EndNr
	import os, subprocess, shutil
	warnings.filterwarnings('ignore')
	# ParseMic for each layer
	topParamFile = data.get('paramFile')
	OrigFileName = data.get('OrigFileName')
	startLayerNr = int(data.get('startLayerNr'))
	endLayerNr = int(data.get('endLayerNr'))
	TopDataDirectory = data.get('TopDataDirectory')
	PFStem = '.'.join(topParamFile.split('.')[:-1])
	Folder = 'Analysis/' + '/'.join(OrigFileName.split('/')[:-1])
	for layerNr in range(startLayerNr,endLayerNr+1):
		newFolder = TopDataDirectory+'/'+Folder+'_Layer_'+str(layerNr)+'/'
		os.chdir(newFolder)
		thisParamFile = PFStem + '_Layer_' + str(layerNr) + '.txt'
		subprocess.call(os.path.expanduser('~/opt/MIDAS/NF_HEDM/bin/ParseMic')+' '+thisParamFile,shell=True)
	os.chdir(TopDataDirectory)
	subprocess.call('tar -czf recon_'+timePath+'.tar.gz '+Folder+'_Layer_{'+str(startLayerNr)+'..'+str(endLayerNr)+'}/Microstructure_Text_*.mic*',shell=True)
	return 'done'

@generate_flow_definition(modifiers={
    nf_remote_parsemic: {'WaitTime': 7200}
})
class NfRemoteParsemic(GladierBaseTool):

    required_input = [
        'paramFile',
        'startLayerNr',
        'endLayerNr',
        'OrigFileName',
        'TopDataDirectory',
        'funcx_endpoint_compute',
    ]

    funcx_functions = [
        nf_remote_parsemic
    ]
