from gladier_hedm.deployments import deployment_map
import datetime

def setup_input(args):
	paramFN = args.paramFile
	thisT = datetime.datetime.now()
	tod = datetime.date.today()
	timePath = str(tod.year) + '_' + str(tod.month).zfill(2) + '_' + str(tod.day).zfill(2) + '_' + str(thisT.hour).zfill(2) + '_' + str(thisT.minute).zfill(2) + '_' + str(thisT.second).zfill(2)
	# ~ timePath = '2022_02_22_14_20_37'
	paramContents = open(paramFN).readlines()
	for line in paramContents:
		if line.startswith('StartFileNrFirstLayer'):
			startNrFirstLayer = int(line.split()[1])
		if line.startswith('NrFilesPerSweep'):
			nrFilesPerSweep = int(line.split()[1])
		if line.startswith('FileStem'):
			fileStem = line.split()[1]
		if line.startswith('StartNr'):
			startNr = int(line.split()[1])
		if line.startswith('EndNr'):
			endNr = int(line.split()[1])
		if line.startswith('ResultDir'):
			rawDir = line.split()[1]
		if line.startswith('DarkFN'):
			darkFN = line.split()[1]
	nFrames = endNr - startNr + 1

	depl = deployment_map.get(args.deployment)
	depl_input = depl.get_input()
	
	## Set up paths
	sourcePath = rawDir
	executePath = depl_input['input']['remote_dir'] + '/' + args.experimentName + '/Analysis/ff/' # Add the experiment name here to get a new execute path
	executeResultPath = executePath+'recon_'+timePath+'.tar.gz'
	resultPath = sourcePath + '/recon_'+timePath+'.tar.gz'
	seedFolder = executePath
	rawFolder = depl_input['input']['remote_dir'] + '/' + args.experimentName + '/ge/'

	## Set up input
	inp = {}
	inp.update({'sourceEP':depl_input['input']['globus_endpoint_source']})
	inp.update({'sourceNCEP':depl_input['input']['globus_endpoint_source_noncompute']})
	inp.update({'procNCEP':depl_input['input']['globus_endpoint_proc_noncompute']})
	inp.update({'portal_id':depl_input['input']['portal_id']})
	inp.update({'sourcePath':sourcePath})
	inp.update({'remoteDataEP':depl_input['input']['globus_endpoint_proc']})
	inp.update({'compute_endpoint':depl_input['input']['compute_endpoint']})
	inp.update({'executePath':executePath})
	inp.update({'executeResultPath':executeResultPath})
	inp.update({'destEP':depl_input['input']['globus_endpoint_result']})
	inp.update({'resultPath':resultPath})
	inp.update({'pfName':paramFN})
	inp.update({'startLayerNr':int(args.startLayerNr)})
	inp.update({'endLayerNr':int(args.endLayerNr)})
	inp.update({'nFrames':nFrames})
	inp.update({'numProcs':int(args.nCPUs)})
	inp.update({'numBlocks':int(args.numNodes)})
	inp.update({'timePath':timePath})
	inp.update({'startNrFirstLayer':startNrFirstLayer})
	inp.update({'nrFilesPerSweep':nrFilesPerSweep})
	inp.update({'fileStem':fileStem})
	inp.update({'seedFolder':seedFolder})
	inp.update({'rawFolder':rawFolder})
	inp.update({'darkFN':darkFN})
	inp.update({'startNr':startNr})
	inp.update({'endNr':endNr})
	inp.update({'experimentName':args.experimentName})

	return inp
