# Example: anapy3 ~/opt/gladier-hedm/scripts/run_ff_flow.py -nCPUs=32 -experimentName=mpe_feb21 -numNodes=10 -startLayerNr=1 -endLayerNr=1 -paramFile=ps_ff_template.txt -deployment=polaris-clutch

from gladier_hedm.flows import FFFlow
from gladier_hedm.flows import FFFlow_SingleNode
from gladier_hedm.setup_payloads import SetupPayloads
from gladier_hedm.setup_input import setup_input
import argparse
from pprint import pprint

def arg_parse():
	parser = argparse.ArgumentParser(description='''MIDAS_FF
	hsharma@anl.gov
	Parameter file, RawFiles (signal and dark) must be in the same folder(RawDir)
	SeedFolder, RawFolder, Dark must not be present
	DarkFN, RawDir should be given
	Run from the same folder as the parameter file (names must match).''', formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument('-nCPUs',type=int, required=True, help='Number of CPU cores per node to use')
	parser.add_argument('-experimentName',type=str, required=True, help='experiment Name for analysis')
	parser.add_argument('-numNodes',type=int, required=True, help='Number of nodes to use')
	parser.add_argument('-startLayerNr',type=int,required=True,help='Start Layer Number')
	parser.add_argument('-endLayerNr',type=int,required=True,help='End Layer Number')
	parser.add_argument('-paramFile',type=str, required=True, help='ParameterFileName')
	parser.add_argument('-deployment',type=str, required=True, help='Locations to run. Available: polaris-clutch, theta-clutch, theta-voyager, edtb-clutch')
	return parser.parse_args()

if __name__ == '__main__':

	args = arg_parse()
	inp = setup_input(args)
	flow_input = SetupPayloads(inp)
	pprint(flow_input)

	ff_cli = FFFlow()
	pprint(ff_cli.flow_definition)
	ff_flow = ff_cli.run_flow(flow_input = flow_input)
	action_id = ff_flow['action_id']
	ff_cli.progress(action_id)
	pprint(ff_cli.get_status(action_id))

	# ~ ff_single_node = FFFlow_SingleNode()
	# ~ pprint(ff_single_node.flow_definition)
	# ~ ff_flow_single_node = ff_single_node.run_flow(flow_input = flow_input)
	# ~ action_id = ff_flow_single_node['action_id']
	# ~ ff_single_node.progress(action_id)
	# ~ pprint(ff_single_node.get_status(action_id))
