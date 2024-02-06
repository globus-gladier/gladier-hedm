from gladier_hedm.deployments import deployment_map
import datetime

def setup_nf_input(args):
	paramFN = args.paramFile
	thisT = datetime.datetime.now()
	tod = datetime.date.today()
	timePath = str(tod.year) + '_' + str(tod.month).zfill(2) + '_' + str(tod.day).zfill(2) + '_' + str(thisT.hour).zfill(2) + '_' + str(thisT.minute).zfill(2) + '_' + str(thisT.second).zfill(2)
	# ~ timePath = '2022_02_22_14_20_37'
	paramContents = open(paramFN).readlines()
	for line in paramContents:
		if line.startswith('ResultDir'):
			rawDir = line.split()[1]
		if line.startswith('nDistances'):
			nDistances = int(line.split()[1])
		if line.startswith('OrigFileName'):
			OrigFileName = line.split()[1]

	depl = deployment_map.get(args.deployment)
	depl_input = depl.get_input()
	
	## Set up paths
	sourcePath = rawDir
	executePath = depl_input['input']['remote_dir'] + '/' + args.experimentName + '/Analysis/nf/' # This will be where it copies the paramFile and Grains.csv
	TopDataDirectory = depl_input['input']['remote_dir'] + '/' + args.experimentName
	executeResultPath = TopDataDirectory+'/Analysis/nf/'+'recon_'+timePath+'.tar.gz'
	resultPath = sourcePath + '/recon_'+timePath+'.tar.gz'

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
	inp.update({'TopDataDirectory':TopDataDirectory})
	inp.update({'OrigFileName':OrigFileName})
	inp.update({'executeResultPath':executeResultPath})
	inp.update({'destEP':depl_input['input']['globus_endpoint_result']})
	inp.update({'resultPath':resultPath})
	inp.update({'pfName':paramFN})
	inp.update({'startLayerNr':int(args.startLayerNr)})
	inp.update({'endLayerNr':int(args.endLayerNr)})
	inp.update({'numProcs':int(args.nCPUs)})
	inp.update({'numBlocks':int(args.numNodes)})
	inp.update({'nDistances':nDistances})
	inp.update({'timePath':timePath})
	inp.update({'FF_Seed':args.FF_Seed})
	inp.update({'experimentName':args.experimentName})

	return inp
