# Generate FF Flow

from gladier import GladierBaseClient, generate_flow_definition


@generate_flow_definition(modifiers={
})
class FFFlow(GladierBaseClient):
    gladier_tools = [
        # ~ 'gladier_hedm.tools.transfer_inject.Inject',
        # ~ 'gladier_hedm.tools.remote_prepare.RemotePrepare',
        # ~ 'gladier_hedm.tools.remote_peaksearch.RemotePeaksearch',   #### Multi - node
        # ~ 'gladier_hedm.tools.remote_transforms.RemoteTransforms',
        # ~ 'gladier_hedm.tools.remote_indexrefine.RemoteIndexrefine', #### Multi - node
        # ~ 'gladier_hedm.tools.remote_process.RemoteFindGrains',
        'gladier_hedm.tools.transfer_extract.Extract',
        'gladier_hedm.tools.remote_publish.Publish'
    ]


@generate_flow_definition(modifiers={
})
class FFFlow_SingleNode(GladierBaseClient):
    gladier_tools = [
        'gladier_hedm.tools.transfer_inject.Inject',
        'gladier_hedm.tools.remote_ff_single_node.RemoteFFSingleNode',
        'gladier_hedm.tools.transfer_extract.Extract',
        'gladier_hedm.tools.remote_publish.Publish'
    ]
