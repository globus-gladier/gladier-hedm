# Example: anapy3 ~/opt/gladier-hedm/scripts/run_nf_flow.py -nCPUs=32 -experimentName=mpe_feb21 -numNodes=10 -startLayerNr=1 -endLayerNr=1 -paramFile=ps_nf_template.txt -deployment=polaris-clutch

from gladier_hedm.flows import NFFlow
from gladier_hedm.setup_nf_payloads import SetupNFPayloads
from gladier_hedm.setup_nf_input import setup_nf_input
import argparse
from pprint import pprint

def arg_parse():
	parser = argparse.ArgumentParser(description='''MIDAS_NF
	hsharma@anl.gov
	Multiple Layers always
	The following parameters should NOT be in the ParametersFile.txt file: 
	RawStartNr, GlobalPosition, MicFileBinary, MicFileText, ReducedFileName, GrainsFile, SeedOrientations, DataDirectory, FullSeedFile
	The following parameters must be present:
	OrigFileName, OverallStartNr, GlobalPositionFirstLayer, LayerThickness, WFImages, nDistances, NrFilesPerDistance
	DO NOT ADD TopDataDirectory to the Parameter File
	OrigFileName in the parameter file must be nf/dataset/filestem (just before the underscore)
	experimentName must match data folder name.
	In case FF_Seed is used, Grains.csv file must exist with parameter file in the result folder''', formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument('-nCPUs',type=int, required=True, help='Number of CPU cores per node to use')
	parser.add_argument('-experimentName',type=str, required=True, help='experiment Name for analysis')
	parser.add_argument('-numNodes',type=int, required=True, help='Number of nodes to use')
	parser.add_argument('-startLayerNr',type=int,required=True,help='Start Layer Number')
	parser.add_argument('-endLayerNr',type=int,required=True,help='End Layer Number')
	parser.add_argument('-paramFile',type=str, required=True, help='ParameterFileName')
	parser.add_argument('-FF_Seed',type=int, required=True, help='FF_Seed')
	parser.add_argument('-deployment',type=str, required=True, help='Locations to run. Available: polaris-clutch, theta-clutch, theta-voyager, edtb-clutch')
	return parser.parse_args()

if __name__ == '__main__':

	args = arg_parse()
	inp = setup_nf_input(args)
	flow_input = SetupNFPayloads(inp)
	pprint(flow_input)

	nf_cli = NFFlow()
	pprint(nf_cli.flow_definition)
	nf_flow = nf_cli.run_flow(flow_input = flow_input)
	action_id = nf_flow['action_id']
	nf_cli.progress(action_id)
	pprint(nf_cli.get_status(action_id))
