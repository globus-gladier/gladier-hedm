from gladier_hedm.flows.ff_flow import FFFlow
from gladier_hedm.endpoints import deployment_map
import gladier_hedm.setup_payloads
import time, json, sys, os, copy
import datetime
import argparse


def arg_parse():
	parser = argparse.ArgumentParser(description='''MIDAS_FF, Parameter file must be in the same folder as the desired output folder(SeedFolder)''', formatter_class=RawTextHelpFormatter)
	parser.add_argument('-nCPUs',    type=int, required=True, help='Number of CPU cores per node to use')
	parser.add_argument('-numNodes',    type=int, required=True, help='Number of nodes to use')
	parser.add_argument('-startLayerNr',type=int,required=True,help='Start Layer Number')
	parser.add_argument('-endLayerNr',type=int,required=True,help='End Layer Number')
	parser.add_argument('-paramFile', type=str, required=True, help='ParameterFileName')
	parser.add_argument('--deployment','-d', default=None, type=str, help=f'Locations to run. Available: {list(deployment_map.keys())}')
	return parser.parse_known_args()

if __name__ == '__main__':

	args, unparsed = arg_parse


	paramFN = args.paramFile
	startLayerNr = int(args.startLayerNr)
	endLayerNr = int(args.endLayerNr)
	numProcs = int(args.nCPUs)
	numBlocks = int(args.numNodes)


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
			endNr = int(line.split()[1])
	nFrames = endNr - startNr + 1
	sourcePath = rawDir

	depl = deployment_map.get(args.deployment)
	depl_input = depl.get_input()
	
	## Set up paths
	sourcePath = rawDir
	executePath = depl_input['input']['remote_dir']
	executeResultPath = executePath+'recon_'+timePath+'.tar.gz'
	resultPath = sourcePath + 'recon_'+timePath+'.tar.gz'
	seedFolder = executePath

	## Set up payloads
	flow_input = setup_payloads(paramFN,startLayerNr,endLayerNr,)


