import yaml
import os

class Config:
    """
    Class that handles config files.

    We have two types of config files :
     - config_params : contains all config parameters about the model
     - infra_params : contains parameters concerning the infra (io folder, logger, etc...)

     config param are callable from a Config object like we would call a dictionnary
    """

    def __init__(self):
        self._infra_params = {}
        self.load_infra_params()

        self.params = {}
        self.load_config_params()
        return

    def _get_infra_params(self):
        return self._infra_params

    def _set_infra_params(self, v):
        self._infra_params = v

    infra_params = property(fget=_get_infra_params, fset=_set_infra_params)

    def load_infra_params(self):
        print(os.getcwd())
        # check if it is develop or deploy
        with open('./conf/infra_params.yml', 'r') as stream:
            self.infra_params = yaml.load(stream)

    def load_config_params(self):
        # check if it is develop or deploy
        with open('./conf/config.yml', 'r') as stream:
            self.params = yaml.load(stream)

    def __getitem__(self, key):
        return self.params[key]