from gladier import GladierBaseTool, generate_flow_definition

def nf_remote_mmap(**data):  #paramFileName startLayerNr endLayerNr timePath StartFileNrFirstLayer NrFilesPerSweep FileStem SeedFolder StartNr EndNr
	import os, subprocess, shutil
	# MMapImageInfo for each layer
	topParamFile = data.get('paramFile')
	OrigFileName = data.get('OrigFileName')
	startLayerNr = int(data.get('startLayerNr'))
	endLayerNr = int(data.get('endLayerNr'))
	TopDataDirectory = data.get('TopDataDirectory')
	timePath = data.get('TimePath')
	PFStem = '.'.join(topParamFile.split('.')[:-1])
	subFolder = TopDataDirectory+'/Analysis/nf/'
	Folder = OrigFileName.split('/')[-2]
	for layerNr in range(startLayerNr,endLayerNr+1):
		newFolder = subFolder+'/'+Folder+'_Layer_'+str(layerNr)+'/'
		os.chdir(newFolder)
		thisParamFile = PFStem + '_Layer_' + str(layerNr) + '.txt'
		subprocess.call(os.path.expanduser('~/opt/MIDAS/NF_HEDM/bin/MMapImageInfo')+' '+thisParamFile,shell=True)
	return 'done'

@generate_flow_definition(modifiers={
    nf_remote_mmap: {'WaitTime': 7200}
})
class NfRemoteMmap(GladierBaseTool):

    required_input = [
		'timePath',
        'paramFile',
        'startLayerNr',
        'endLayerNr',
        'OrigFileName',
        'TopDataDirectory',
        'funcx_endpoint_compute',
    ]

    funcx_functions = [
        nf_remote_mmap
    ]
