
class BaseDeployment:
    globus_endpoints = dict()
    funcx_endpoints = dict()
    flow_input = dict()

    def get_input(self):
        fi = self.flow_input.copy()
        fi['input'].update(self.funcx_endpoints)
        fi['input'].update(self.globus_endpoints)
        return fi

class OrthrosClutchDeployment(BaseDeployment):

    globus_endpoints = {
        'globus_endpoint_source': 'b0e921df-6d04-11e5-ba46-22000b92c6ec',
        'globus_endpoint_proc': 'b0e921df-6d04-11e5-ba46-22000b92c6ec',
        'globus_endpoint_result': 'b0e921df-6d04-11e5-ba46-22000b92c6ec',
    }

    funcx_endpoints = {
        'funcx_endpoint_compute': '29570327-867e-431c-acac-35e89296845e',
    }

    flow_input = {
        'input': {
            'remote_dir': '/data/tomo1/funcx_jobs/',
            'source_dir': '/data/tomo1/',
        }
    }

class ThetaClutchDeployment(BaseDeployment):

    globus_endpoints = {
        'globus_endpoint_source': 'b0e921df-6d04-11e5-ba46-22000b92c6ec',
        'globus_endpoint_proc': '08925f04-569f-11e7-bef8-22000b9a448b',
        'globus_endpoint_result': 'b0e921df-6d04-11e5-ba46-22000b92c6ec',
    }

    funcx_endpoints = {
        'funcx_endpoint_compute': '29570327-867e-431c-acac-35e89296845e',
    }

    flow_input = {
        'input': {
            'remote_dir': '/lus/theta-fs0/projects/APSPolarisI2E/HEDM/',
            'source_dir': '/data/tomo1/',
        }
    }

class CooleyThetaClutchDeployment(BaseDeployment):

    globus_endpoints = {
        'globus_endpoint_source': 'b0e921df-6d04-11e5-ba46-22000b92c6ec',
        'globus_endpoint_proc': '08925f04-569f-11e7-bef8-22000b9a448b',
        'globus_endpoint_result': 'b0e921df-6d04-11e5-ba46-22000b92c6ec',
    }

    funcx_endpoints = {
        'funcx_endpoint_compute': '60565a3a-a7df-4ae2-b98b-4f91bec4b288',
    }

    flow_input = {
        'input': {
            'remote_dir': '/lus/theta-fs0/projects/APSPolarisI2E/HEDM/',
            'source_dir': '/data/tomo1/',
        }
    }

class ThetaVoyagerDeployment(BaseDeployment):

    globus_endpoints = {
        'globus_endpoint_source': '9c9cb97e-de86-11e6-9d15-22000a1e3b52',
        'globus_endpoint_proc': '08925f04-569f-11e7-bef8-22000b9a448b',
        'globus_endpoint_result': 'b0e921df-6d04-11e5-ba46-22000b92c6ec',
    }

    funcx_endpoints = {
        'funcx_endpoint_compute': '29570327-867e-431c-acac-35e89296845e',
    }

    flow_input = {
        'input': {
            'remote_dir': '/lus/theta-fs0/projects/APSPolarisI2E/HEDM/',
            'source_dir': '/gdata/dm/1ID/2021/',
        }
    }


deployment_map = {
    'cooley-theta-clutch': CooleyThetaClutchDeployment(),
    'theta-clutch': ThetaClutchDeployment(),
    'theta-voyager': ThetaVoyagerDeployment(),
}
