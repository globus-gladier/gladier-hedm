from gladier import GladierBaseTool, generate_flow_definition

def nf_remote_prepare(**data):  #paramFileName startLayerNr endLayerNr timePath StartFileNrFirstLayer NrFilesPerSweep FileStem SeedFolder StartNr EndNr
	# Prepare for each layer
	import os, subprocess, shutil
	from pathlib import Path
	import numpy as np
	
	warnings.filterwarnings('ignore')
	def getValueFromParamFile(paramfn,searchStr,nLines=1,wordNr=1,nWords=1):
		ret_list = []
		nrLines = 0
		f = open(paramfn,'r')
		PSContents = f.readlines()
		f.close()
		for line in PSContents:
			if line.startswith(searchStr+' '):
				words = line.replace('\t',' ').replace('\n',' ').split(' ')
				words = [_f for _f in words if _f]
				ret_list.append(words[wordNr:wordNr+nWords])
				nrLines += 1
				if (nrLines == nLines):
					return ret_list
		return ret_list
	
	# Get params
	topParamFile = data.get('paramFile')
	startLayerNr = int(data.get('startLayerNr'))
	endLayerNr = int(data.get('endLayerNr'))
	FF_Seed = int(data.get('FF_Seed'))
	TopDataDirectory = data.get('TopDataDirectory')
	OrigFileName = data.get('OrigFileName')
	
	# Initial setup
	extOrig = getValueFromParamFile(topParamFile,'extOrig')[0][0]
	FullSeedFile = getValueFromParamFile(topParamFile,'FullSeedFile')[0][0]
	OverallStartNr = int(getValueFromParamFile(topParamFile,'OverallStartNr')[0][0])
	GlobalPositionFirstLayer = int(getValueFromParamFile(topParamFile,'GlobalPositionFirstLayer')[0][0])
	LayerThickness = int(getValueFromParamFile(topParamFile,'LayerThickness')[0][0])
	WFImages = int(getValueFromParamFile(topParamFile,'WFImages')[0][0])
	nDistances = int(getValueFromParamFile(topParamFile,'nDistances')[0][0])
	NrFilesPerDistance = int(getValueFromParamFile(topParamFile,'NrFilesPerDistance')[0][0])
	FStem = OrigFileName.split('/')[-1]
	Folder = 'Analysis/' + '/'.join(OrigFileName.split('/')[:-1])
	PFStem = '.'.join(topParamFile.split('.')[:-1])
	NrFilesPerLayer = (NrFilesPerDistance+WFImages)*nDistances
	subFolder = TopDataDirectory+'/Analysis/nf'
	DoGrid = 1
	
	os.chdir(TopDataDirectory)
	with open(topParamFile) as tpf:
		paramContents = tpf.readlines()
	
	for layerNr in range(startLayerNr,endLayerNr+1):
		newFolder = TopDataDirectory+'/'+Folder+'_Layer_'+str(layerNr)+'/'
		subprocess.call('mkdir -p '+newFolder+Folder,shell=True)
		os.chdir(newFolder)
		startFileNrThisLayer = str((layerNr-1)*NrFilesPerLayer+OverallStartNr).zfill(6)
		endFileNrThisLayer = str(startFileNrThisLayer + NrFilesPerLayer - 1).zfill(6)
		if !os.path.isfile(newFolder+'/'+Folder+'/'+FStem+'_'+startFileNrThisLayer+'.'+extOrig) and !os.path.isfile(newFolder+'/'+Folder+'/'+FStem+'_'+endFileNrThisLayer+'.'+extOrig):
			subprocess.call('mv '+TopDataDirectory+'/'+OrigFileName+'_{'+startFileNrThisLayer+'..'+endFileNrThisLayer+'.'+extOrig+' '+newFolder+'/'+Folder,shell=True)
		positionThisLayer = GlobalPositionFirstLayer + LayerThickness*(layerNr-1)
		thisParamFile = PFStem + '_Layer_' + str(layerNr) + '.txt'
		reducedFolder = Folder+'_Layer'str(layerNr)+'_Reduced/'
		f = open(thisParamFile,'w')
		for line in paramContents:
			f.write(line)
		f.write('RawStartnr '+str(startFileNrThisLayer)+'\n')
		f.write('GlobalPosition '+str(positionThisLayer)+'\n')
		f.write('MicFileBinary Microstructure_Binary_Layer'+str(layerNr)+'.mic\n')
		f.write('MicFileText Microstructure_Text_Layer'+str(layerNr)+'.mic\n')
		f.write('ReducedFileName '+reducedFolder+FStem+'\n')
		f.write('DataDirectory '+newFolder+'\n')
		subprocess.call('mkdir -p '+reducedFolder,shell=True)
		if FF_Seed == 1:
			subprocess.call('cp '+TopDataDirectory+'/Analysis/nf/Grains.csv '+newFolder,shell=True)
			if os.path.isfile(TopDataDirectory+'/Analysis/nf/OrientationsAll.txt'):
				subprocess.call('cp '+TopDataDirectory+'/Analysis/nf/OrientationsAll.txt '+newFolder,shell=True)
				f.write('FullSeedFile '+newFolder+'/OrientationsAll.txt\n')
			f.write('GrainsFile '+newFolder+'/Grains.csv\n')
			f.write('SeedOrientations '+newFolder+'/Orientations_Layer_'+str(layerNr)+'.txt\n')
		else:
			subprocess.call('cp '+TopDataDirectory+'/Analysis/nf/OrientationsAll.txt '+newFolder+'/Orientations.txt',shell=True)
			f.write('SeedOrientations '+newFolder+'/Orientations.txt\n')
		f.close()
		subprocess.call('rm -rf output Microstructure*',shell=True)
		subprocess.call(os.path.expanduser('~/opt/MIDAS/NF_HEDM/bin/GetHKLList')+' '+thisParamFile,shell=True)
		if FF_Seed == 1:
			SeedOrientations = getValueFromParamFile(thisParamFile,'SeedOrientations')[0][0]
			GrainsFile = getValueFromParamFile(thisParamFile,'GrainsFile')[0][0]
			subprocess.call(os.path.expanduser('~/opt/MIDAS/NF_HEDM/bin/GenSeedOrientationsFF2NFHEDM')+' '+GrainsFile+' '+SeedOrientations,shell=True)
		with open(SeedOrientations) as so:
			NrOrients = len(so.readlines())
		f = open(thisParamFile,'a')
		f.write('NrOrientations ',str(NrOrients)+'\n')
		f.close()
		if DoGrid == 1:
			subprocess.call(os.path.expanduser('~/opt/MIDAS/NF_HEDM/bin/MakeHexGrid')+' '+thisParamFile,shell=True)
			tomoF = getValueFromParamFile(thisParamFile,'TomoImage')
			if len(tomoF) > 0:
				tomoPxSize = getValueFromParamFile(thisParamFile,'TomoPixelSize')
				subprocess.call(os.path.expanduser('~/opt/MIDAS/NF_HEDM/bin/filterGridfromTomo')+' '+tomoF+' '+tomoPxSize,shell=True)
				subprocess.call('mv grid.txt grid_unfilt.txt',shell=True)
				subprocess.call('mv gridNew.txt grid.txt',shell=True)
			else:
				gm = getValueFromParamFile(thisParamFile,'GridMask')
				if (len(gm > 0)):
					gmSz = getValueFromParamFile(thisParamFile,'GridMask',1,1,4)
					grid_vals = np.genfromtxt('grid.txt',skip_header=1)
					subprocess.call('mv grid.txt grid_old.txt',shell=True)
					grid_vals = grid_vals[:,2]>=float(gmSz[0])
					grid_vals = grid_vals[:,2]<=float(gmSz[1])
					grid_vals = grid_vals[:,3]<=float(gmSz[2])
					grid_vals = grid_vals[:,3]<=float(gmSz[3])
					head_grid = str(grid_vals.shape[0])
					f_grid = open('grid.txt','w')
					f_grid.write(head_grid+'\n')
					f_grid.close()
					f_grid = open('grid.txt','a')
					np.savetxt(f_grid,grid_vals,fmt='%.6f',delimiter=' ',newline='\n')
					f_grid.close()
		subprocess.call(os.path.expanduser('~/opt/MIDAS/NF_HEDM/bin/MakeDiffrSpots')+' '+thisParamFile,shell=True)
	return 'done'

@generate_flow_definition(modifiers={
    nf_remote_prepare: {'WaitTime': 7200}
})
class NfRemotePrepare(GladierBaseTool):

    required_input = [
        'paramFile',
        'startLayerNr',
        'endLayerNr',
        'OrigFileName',
        'TopDataDirectory',
        'FF_Seed',
        'funcx_endpoint_compute',
    ]

    funcx_functions = [
        nf_remote_prepare
    ]
