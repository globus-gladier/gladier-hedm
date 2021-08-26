# Generate FF Flow

from gladier import GladierBaseClient, generate_flow_definition


@generate_flow_definition(modifiers={
})
class FFFlow(GladierBaseClient):
    #globus_group = '' # Later

    gladier_tools = [
        'galdier_hedm.tools.transfer_inject.Inject',
        'galdier_hedm.tools.remote_prepare.RemotePrepare',
        'galdier_hedm.tools.remote_peaksearch.RemotePeaksearch',
        'galdier_hedm.tools.remote_transforms.RemoteTransforms',
        'galdier_hedm.tools.remote_indexrefine.RemoteIndexrefine',
        'galdier_hedm.tools.remote_process.RemoteFindGrains',
        'galdier_hedm.tools.transfer_extract.Extract',
    ]
