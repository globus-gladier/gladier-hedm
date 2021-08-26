from gladier_hedm.flows.ff_flow import FFFlow
from gladier_hedm.endpoints import deployment_map
from gladier_hedm.setup_payloads import SetupPayloads
import time, json, sys, os, copy
import datetime
import argparse
import pprint

def arg_parse():
	parser = argparse.ArgumentParser(description='''MIDAS_FF, Parameter file must be in the same folder as the desired output folder(SeedFolder)''', formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument('-nCPUs',    type=int, required=True, help='Number of CPU cores per node to use')
	parser.add_argument('-experimentName',    type=str, required=True, help='experiment Name for analysis')
	parser.add_argument('-numNodes',    type=int, required=True, help='Number of nodes to use')
	parser.add_argument('-startLayerNr',type=int,required=True,help='Start Layer Number')
	parser.add_argument('-endLayerNr',type=int,required=True,help='End Layer Number')
	parser.add_argument('-paramFile', type=str, required=True, help='ParameterFileName')
	parser.add_argument('-deployment', type=str, required=True, help='Locations to run. Available: theta-clutch, theta-voyager')
	return parser.parse_args()

if __name__ == '__main__':

	args = arg_parse()


	paramFN = args.paramFile
	startLayerNr = int(args.startLayerNr)
	endLayerNr = int(args.endLayerNr)
	numProcs = int(args.nCPUs)
	numBlocks = int(args.numNodes)
	experimentName = args.experimentName


	thisT = datetime.datetime.now()
	tod = datetime.date.today()
	timePath = str(tod.year) + '_' + str(tod.month).zfill(2) + '_' + str(tod.day).zfill(2) + '_' + str(thisT.hour).zfill(2) + '_' + str(thisT.minute).zfill(2) + '_' + str(thisT.second).zfill(2)
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
		if line.startswith('RawDir'):
			rawDir = line.split()[1]
	nFrames = endNr - startNr + 1

	depl = deployment_map.get(args.deployment)
	depl_input = depl.get_input()
	
	## Set up paths
	sourcePath = rawDir
	executePath = depl_input['input']['remote_dir']
	executeResultPath = executePath+'recon_'+timePath+'.tar.gz'
	resultPath = sourcePath + 'recon_'+timePath+'.tar.gz'
	seedFolder = executePath

	## Set up payloads
	inp = {}
	inp.update({'sourceEP':depl_input['input']['globus_endpoint_source']})
	inp.update({'sourcePath':sourcePath})
	inp.update({'remoteDataEP':depl_input['input']['globus_endpoint_proc']})
	inp.update({'funcx_endpoint_compute':depl_input['input']['funcx_endpoint_compute']})
	inp.update({'executePath':executePath})
	inp.update({'executeResultPath':executeResultPath})
	inp.update({'destEP':depl_input['input']['globus_endpoint_result']})
	inp.update({'resultPath':resultPath})
	inp.update({'pfName':paramFN})
	inp.update({'startLayerNr':startLayerNr})
	inp.update({'endLayerNr':endLayerNr})
	inp.update({'nFrames':nFrames})
	inp.update({'numProcs':numProcs})
	inp.update({'numBlocks':numBlocks})
	inp.update({'timePath':timePath})
	inp.update({'startNrFirstLayer':startNrFirstLayer})
	inp.update({'nrFilesPerSweep':nrFilesPerSweep})
	inp.update({'fileStem':fileStem})
	inp.update({'seedFolder':seedFolder})
	inp.update({'startNr':startNr})
	inp.update({'endNr':endNr})
	
	flow_input = SetupPayloads(inp)
	# ~ print(flow_input)
	
	ff_cli = FFFlow()
	pprint(ff_cli.flow_definition)
	# ~ ff_flow_label = f'{experimentName}_{fileStem}_{startLayerNr}_{endLayerNr}'
	
	# ~ ff_flow = ff_cli.run_flow(flow_input = flow_input, label = ff_flow_label)
	# ~ action_id = ff_flow['action_id']
	# ~ ff_cli.progress(action_id)
	# ~ pprint(ff_cli.get_status(action_id))

	# ~ print('run_id : ' + ff_flow['action_id'])

