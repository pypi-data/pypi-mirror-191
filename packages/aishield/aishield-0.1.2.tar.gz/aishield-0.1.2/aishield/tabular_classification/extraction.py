from aishield.constants import Attack
from aishield.tabular_classification.base_tc import TCVulnerabilityConfig
from aishield.utils.util import delete_keys_from_dict


class VulnConfig(TCVulnerabilityConfig):
    def __init__(self, defense_generate):
        super().__init__(defense_generate)
        self.attack_type = 'blackbox'
        self.attack = Attack.EXTRACTION

    @property
    def attack_type(self):
        return self.__attack_type

    @attack_type.setter
    def attack_type(self, attack_type):
        self.__attack_type = attack_type

    def get_all_params(self):
        params = super(VulnConfig, self).get_all_params()
        params = delete_keys_from_dict(params, ['task_type', 'attack'])
        return params
