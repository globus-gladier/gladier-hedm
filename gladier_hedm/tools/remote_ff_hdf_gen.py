from gladier import GladierBaseTool, generate_flow_definition

def remote_ff_hdf_gen(**data):
	import os
	import numpy as np
	import h5py
	import warnings
	import matplotlib.pyplot as plt

	warnings.filterwarnings('ignore')
	def getValueFromParamFile(paramfn,searchStr,nLines=1,wordNr=1,nWords=1):
		ret_list = []
		nrLines = 0
		f = open(paramfn,'r')
		PSContents = f.readlines()
		for line in PSContents:
			if line.startswith(searchStr+' '):
				words = line.replace('\t',' ').replace('\n',' ').split(' ')
				words = [_f for _f in words if _f]
				ret_list.append(words[wordNr:wordNr+nWords])
				nrLines += 1
				if (nrLines == nLines):
					return ret_list
		return ret_list

	startLayerNr = int(data.get('startLayerNr'))
	endLayerNr = int(data.get('endLayerNr'))
	time_path = data.get('timePath')
	fStem = data.get('FileStem')
	topdir = data.get('SeedFolder')
	paramFile = data.get('paramFileName')
	headSpots = 'GrainID SpotID Omega DetectorHor DetectorVert OmeRaw Eta RingNr YLab ZLab Theta StrainError OriginalRadiusFileSpotID IntegratedIntensity Omega(degrees) YCen(px) ZCen(px) IMax MinOme(degrees) MaxOme(degress) Radius(px) Theta(degrees) Eta(degrees) DeltaOmega NImgs RingNr GrainVolume GrainRadius PowderIntensity SigmaR SigmaEta NrPx'
	resArr = []

	for layerNr  in range(startLayerNr,endLayerNr+1):
		thisDir = folderName = fStem + '_Layer_' + str(layerNr).zfill(4) + '_Analysis_Time_' + time_path
		thisDir = topdir + '/' + folderName + '/'
		os.chdir(thisDir)
		outFN = f'{thisDir}/remote_data/result_{fStem}_LayerNr_{layerNr}_Analysis_time_{time_path}.hdf'
		startNr = int(getValueFromParamFile(paramFile,'StartNr')[0][0])
		endNr = int(getValueFromParamFile(paramFile,'EndNr')[0][0])
		pad = int(getValueFromParamFile(paramFile,'Padding')[0][0])
		Grains = np.genfromtxt('Grains.csv',skip_header=9)
		SpotMatrix = np.genfromtxt('SpotMatrix.csv',skip_header=1)
		IDRings = np.genfromtxt('IDRings.csv',skip_header=1)
		IDsHash = np.genfromtxt('IDsHash.csv',skip_header=1)
		InputAll = np.genfromtxt('InputAll.csv',skip_header=1)
		InputAllExtra = np.genfromtxt('InputAllExtraInfoFittingAll.csv',skip_header=1)
		SpotsToIndex = np.genfromtxt('SpotsToIndex.csv',skip_header=1)
		HKLs = np.genfromtxt('hkls.csv',skip_header=1)
		outFile = h5py.File(outFN,'w')

		f = open('Grains.csv','r')
		nGrains = int(f.readline().split()[1])
		beamCenter = float(f.readline().split()[1])
		beamThickness = float(f.readline().split()[1])
		globalPosition = float(f.readline().split()[1])
		f.readline()
		f.readline()
		f.readline()
		f.readline()
		hGr = f.readline()
		f.close()

		outFile.attrs['Software'] = np.string_("MIDAS")
		outFile.attrs['Version'] = np.string_("6.0")
		outFile.attrs['Contact'] = np.string_("hsharma@anl.gov")
		outFile.create_dataset('ParametersFile',data=np.string_(open(paramFile).read()))
		group1 = outFile.create_group('RawFiles')
		group1.create_dataset('paramstest',data=np.string_(open('paramstest.txt').read()))
		sm = group1.create_dataset('SpotMatrix',data=SpotMatrix)
		sm.attrs['head'] = np.string_(open('SpotMatrix.csv').readline())
		gr = group1.create_dataset('AllGrains',data=Grains)
		gr.attrs['head'] = np.string_(hGr)
		idr = group1.create_dataset('IDRings',data=IDRings)
		idr.attrs['head'] = np.string_(open('IDRings.csv').readline())
		idh = group1.create_dataset('IDsHash',data=IDsHash)
		idh.attrs['head'] = np.string_(open('IDsHash.csv').readline())
		ipa = group1.create_dataset('InputAll',data=InputAll)
		ipa.attrs['head'] = np.string_(open('InputAll.csv').readline())
		ipe = group1.create_dataset('InputAllExtraInfo',data=InputAllExtra)
		ipe.attrs['head'] = np.string_(open('InputAllExtraInfoFittingAll.csv').readline())
		group1.create_dataset('SpotsToIndex',data=SpotsToIndex)
		hk = group1.create_dataset('HKLs',data=HKLs)
		hk.attrs['head'] = np.string_(open('hkls.csv').readline())
		
		# We have a merged filesystem now, not according to rings
		# Put Temp data
		group2 = group1.create_group('Temp')
		for fNr in range(startNr,endNr+1):
			fileName = f'{os.getcwd()}/Temp/{fStem}_{layerNr}_{str(fNr).zfill(pad)}_PS.csv'
			if os.path.exists(fileName):
				arr = np.genfromtxt(fileName,skip_header=1)
				if arr.shape[0] > 0:
					tmpd = group3.create_dataset(os.path.basename(fileName),data=arr)
					tmpd.attrs['head'] = np.string_(open(fileName).readline())
		# Put Radii
		fileName = f'{os.getcwd()}/Radius_StartNr_{startNr}_EndNr_{endNr}.csv'
		arr = np.genfromtxt(fileName,skip_header=1)
		nSps,nColsRad = arr.shape
		radd = group1.create_dataset(os.path.basename(fileName),data=arr)
		radd.attrs['head'] = np.string_(open(fileName).readline())
		radii = arr
		# Put Merge Result
		fileName = f'{os.getcwd()}/Result_StartNr_{startNr}_EndNr_{endNr}.csv'
		arr = np.genfromtxt(fileName,skip_header=1)
		nSps,nTrs = arr.shape
		resd = group1.create_dataset(os.path.basename(fileName),data=arr)
		resd.attrs['head'] = np.string_(open(fileName).readline())
		resarr = arr
		
		gg = outFile.create_group('Grains')
		
		for counter,grain in enumerate(Grains):
			thisID = int(grain[0])
			print(f'Processing grain {counter+1} out of {Grains.shape[0]} grains.')
			grg = gg.create_group('GrainID_'+str(thisID))
			grd = grg.create_dataset('GrainInfo',data=grain)
			grd.attrs['header'] = hGr
			spotsThisGrain = SpotMatrix[SpotMatrix[:,0] == thisID]
			RadiusInfo = np.empty((spotsThisGrain.shape[0],nColsRad))
			for ctr,spot in enumerate(spotsThisGrain):
				spotID = int(spot[1])
				orig_ID = int(IDRings[IDRings[:,2]==spotID,1])
				ringNr = int(IDRings[IDRings[:,2]==spotID,0])
				subInfo = radii[orig_ID-1]
				RadiusInfo[ctr,:] = subInfo
			RadiusInfo = np.hstack((spotsThisGrain,RadiusInfo))
			spd = grg.create_dataset('SpotMatrix_Radius',data=RadiusInfo)
			spd.attrs['header'] = headSpots
		outFile.close()
		# Make and save plots
		plt.scatter(Grains[:,10],Grains[:,11]);  plt.xlabel('X [\mu m]'); plt.ylabel('Y [\mu m]'); plt.savefig('remote_data/XY.png'); plt.clf()
		plt.scatter(Grains[:,11],Grains[:,12]);  plt.xlabel('Y [\mu m]'); plt.ylabel('Z [\mu m]'); plt.savefig('remote_data/YZ.png'); plt.clf()
		plt.scatter(Grains[:,10],Grains[:,12]);  plt.xlabel('X [\mu m]'); plt.ylabel('Z [\mu m]'); plt.savefig('remote_data/XZ.png'); plt.clf()
		plt.scatter(Grains[:,19],Grains[:,22]);  plt.xlabel('Grain Radius [\mu m]'); plt.ylabel('PosErr [\mu m]'); plt.savefig('remote_data/PosvsRad.png'); plt.clf()
		plt.scatter(Grains[:,21],Grains[:,22]);  plt.xlabel('Grain Radius [\mu m]'); plt.ylabel('InternalAngle [Degrees]'); plt.savefig('remote_data/IAvsRad.png'); plt.clf()
		plt.scatter(Grains[:,33],Grains[:,22]);  plt.xlabel('Grain Radius [\mu m]'); plt.ylabel('E_XX'); plt.savefig('remote_data/eXXvsRad.png'); plt.clf()
		plt.scatter(Grains[:,37],Grains[:,22]);  plt.xlabel('Grain Radius [\mu m]'); plt.ylabel('E_YY'); plt.savefig('remote_data/eYYvsRad.png'); plt.clf()
		plt.scatter(Grains[:,41],Grains[:,22]);  plt.xlabel('Grain Radius [\mu m]'); plt.ylabel('E_ZZ'); plt.savefig('remote_data/eZZvsRad.png'); plt.clf()
		os.chdir(topdir)
		resArr.append(outFN)
	return(resArr)

@generate_flow_definition(modifiers={
    remote_ff_hdf_gen: {'WaitTime': 7200},
    
})
class RemoteGenerateHDF(GladierBaseTool):

    required_input = [
        'paramFileName',
        'startLayerNr',
        'endLayerNr',
        'timePath',
        'FileStem',
        'SeedFolder',
        'funcx_endpoint_compute',
    ]

    funcx_functions = [
        remote_ff_hdf_gen
    ]
