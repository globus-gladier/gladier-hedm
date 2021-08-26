# Generate FF Flow

from gladier import GladierBaseClient, generate_flow_definition


@generate_flow_definition(modifiers={
})
class FFFlow(GladierBaseClient):
    #globus_group = '' # Later

    gladier_tools = [
        'gladier_hedm.tools.transfer_inject.Inject',
        'gladier_hedm.tools.remote_prepare.RemotePrepare',
        'gladier_hedm.tools.remote_peaksearch.RemotePeaksearch',
        'gladier_hedm.tools.remote_transforms.RemoteTransforms',
        'gladier_hedm.tools.remote_indexrefine.RemoteIndexrefine',
        'gladier_hedm.tools.remote_process.RemoteFindGrains',
        'gladier_hedm.tools.transfer_extract.Extract',
    ]
