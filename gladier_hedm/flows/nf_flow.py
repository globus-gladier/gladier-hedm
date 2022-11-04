# Generate NF Flow

from gladier import GladierBaseClient, generate_flow_definition

@generate_flow_definition(modifiers={
})
class NFFlow(GladierBaseClient):
    gladier_tools = [
        'gladier_hedm.tools.transfer_inject.Inject',
        'gladier_hedm.tools.nf_remote_prepare.NfRemotePrepare',
        'gladier_hedm.tools.nf_remote_median.NfRemoteMedian',   #### Multi - node
        'gladier_hedm.tools.nf_remote_imageprocessing.NfRemoteImageProcessing',   #### Multi - node
        'gladier_hedm.tools.nf_remote_mmap.NfRemoteMmap',
        'gladier_hedm.tools.nf_remote_fitorientation.NfRemoteFitOrientation', #### Multi - node
        'gladier_hedm.tools.nf_remote_parsemic.NfRemoteParsemic',
        'gladier_hedm.tools.transfer_extract.Extract',
        #'gladier_hedm.tools.nf_remote_publish.Publish'
    ]
