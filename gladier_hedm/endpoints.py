
class BaseDeployment:
    globus_endpoints = dict()
    funcx_endpoints = dict()
    flow_input = dict()

    def get_input(self):
        fi = self.flow_input.copy()
        fi['input'].update(self.funcx_endpoints)
        fi['input'].update(self.globus_endpoints)
        return fi

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
        }
    }


deployment_map = {
    'theta-clutch': ThetaClutchDeployment(),
    'theta-voyager': ThetaVoyagerDeployment(),
}