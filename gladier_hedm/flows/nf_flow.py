# Generate NF Flow

from gladier import GladierBaseClient, generate_flow_definition

@generate_flow_definition(modifiers={
})
class NFFlow(GladierBaseClient):
    gladier_tools = [
        'gladier_hedm.tools.transfer_inject.Inject',
        'gladier_hedm.tools.nf_remote_prepare.NfRemotePrepare',
        'gladier_hedm.tools.nf_remote_peaksearch.NfRemoteMedian',   #### Multi - node
        'gladier_hedm.tools.nf_remote_peaksearch.NfRemoteImagePorocessing',   #### Multi - node
        'gladier_hedm.tools.nf_remote_transforms.NfRemoteMmap',
        'gladier_hedm.tools.nf_remote_indexrefine.NfRemoteFitOrientation', #### Multi - node
        'gladier_hedm.tools.nf_remote_process.NfRemoteParseMic',
        'gladier_hedm.tools.transfer_extract.Extract',
        #'gladier_hedm.tools.nf_remote_publish.Publish'
    ]
