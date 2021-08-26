from gladier import GladierBaseTool


class Inject(GladierBaseTool):

    flow_definition = {
        'Comment': 'Inject data',
        'StartAt': 'Inject',
        'States': {
            'Inject': {
                'Comment': 'Inject data',
                'Type': 'Action',
                'ActionUrl': 'https://actions.automate.globus.org/transfer/transfer',
                'Parameters': {
                    'source_endpoint_id.$': '$.input.inject_source_endpoint_id',
                    'destination_endpoint_id.$': '$.input.inject_destination_endpoint_id',
                    'transfer_items': [
                        {
                            'source_path.$': '$.input.inject_source_path',
                            'destination_path.$': '$.input.inject_destination_path',
                            'recursive.$': '$.input.inject_recursive',
                        }
                    ]
                },
                'ResultPath': '$.InjectResult',
                'WaitTime': 1200,
                'End': True
            },
        }
    }

    flow_input = {
        'inject_sync_level': 'checksum'
    }
    required_input = [
        'inject_source_path',
        'inject_destination_path',
        'inject_source_endpoint_id',
        'inject_destination_endpoint_id',
        'inject_recursive',
    ]
