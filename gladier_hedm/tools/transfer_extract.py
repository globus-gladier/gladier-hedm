from gladier import GladierBaseTool


class Extract(GladierBaseTool):

    flow_definition = {
        'Comment': 'Extract data',
        'StartAt': 'Extract',
        'States': {
            'Extract': {
                'Comment': 'Extract reconstructed data',
                'Type': 'Action',
                'ActionUrl': 'https://actions.automate.globus.org/transfer/transfer',
                'Parameters': {
                    'source_endpoint_id.$': '$.input.extract_source_endpoint_id',
                    'destination_endpoint_id.$': '$.input.extract_destination_endpoint_id',
                    'transfer_items': [
                        {
                            'source_path.$': '$.input.extract_source_path',
                            'destination_path.$': '$.input.extract_destination_path',
                            'recursive.$': '$.input.extract_recursive',
                        }
                    ]
                },
                'ResultPath': '$.ExtractResult',
                'WaitTime': 1200,
                'End': True
            },
        }
    }

    flow_input = {
        'extract_sync_level': 'checksum'
    }
    required_input = [
        'extract_source_path',
        'extract_destination_path',
        'extract_source_endpoint_id',
        'extract_destination_endpoint_id',
        'extract_recursive',
    ]
