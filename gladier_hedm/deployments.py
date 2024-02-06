
class BaseDeployment:
    globus_endpoints = dict()
    compute_endpoints = dict()
    flow_input = dict()

    def get_input(self):
        fi = self.flow_input.copy()
        fi['input'].update(self.compute_endpoints)
        fi['input'].update(self.globus_endpoints)
        fi['input'].update(self.portal_ids)
        return fi

class OrthrosClutchDeployment(BaseDeployment):

    globus_endpoints = {
        'globus_endpoint_source': 'b0e921df-6d04-11e5-ba46-22000b92c6ec',
        'globus_endpoint_source_noncompute': '08f6e19f-52d0-4eae-b190-df412518e63a',
        'globus_endpoint_proc': 'b0e921df-6d04-11e5-ba46-22000b92c6ec',
        'globus_endpoint_proc_noncompute': 'b0e921df-6d04-11e5-ba46-22000b92c6ec',
        'globus_endpoint_result': 'b0e921df-6d04-11e5-ba46-22000b92c6ec',
    }

    compute_endpoints = {
        'compute_endpoint': '29570327-867e-431c-acac-35e89296845e',
    }

    portal_ids = {
        'portal_id': '9302766a-aefc-47e9-81d1-34a06f3508f3',
    }

    flow_input = {
        'input': {
            'remote_dir': '/data/tomo1/compute_jobs/',
            'source_dir': '/data/tomo1/',
        }
    }

class PolarisClutchDeployment(BaseDeployment):

    globus_endpoints = {
        'globus_endpoint_source': 'b0e921df-6d04-11e5-ba46-22000b92c6ec',
        'globus_endpoint_source_noncompute': '08f6e19f-52d0-4eae-b190-df412518e63a',
        'globus_endpoint_proc': '08925f04-569f-11e7-bef8-22000b9a448b',
        'globus_endpoint_proc_noncompute': 'e47744d4-a018-4adc-b184-a7d20e4b4738',
        'globus_endpoint_result': 'b0e921df-6d04-11e5-ba46-22000b92c6ec',
    }

    compute_endpoints = {
        'compute_endpoint': 'e9004916-9073-446f-b01d-ce98d7999d6b',
    }

    portal_ids = {
        'portal_id': '9302766a-aefc-47e9-81d1-34a06f3508f3',
    }

    flow_input = {
        'input': {
            'remote_dir': '/lus/eagle/projects/APSDataAnalysis/MIDAS_workshop/',
            'source_dir': '/data/tomo1/',
        }
    }


deployment_map = {
    'polaris-clutch':PolarisClutchDeployment(),
}
