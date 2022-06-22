import unittest

import srl
from srl.test import TestRL


class Test(unittest.TestCase):
    def setUp(self) -> None:
        self.tester = TestRL()
        self.rl_config = srl.rl.agent57_light.Config()
        self.pendulum_config = {
            "hidden_layer_sizes": (128, 128),
            "enable_dueling_network": False,
            "memory_name": "ReplayMemory",
            "target_model_update_interval": 100,
            "actor_num": 8,
            "input_ext_reward": False,
            "input_int_reward": False,
            "input_action": False,
            "enable_intrinsic_reward": True,
        }

    def test_sequence(self):
        self.tester.play_sequence(self.rl_config)

    def test_mp(self):
        self.tester.play_mp(self.rl_config)

    def test_Pendulum(self):
        rl_config = srl.rl.agent57_light.Config(**self.pendulum_config)
        self.tester.play_verify_singleplay("Pendulum-v1", rl_config, 200 * 30)

    def test_Pendulum_mp(self):
        rl_config = srl.rl.agent57_light.Config(**self.pendulum_config)
        rl_config.memory_name = "ProportionalMemory"
        self.tester.play_verify_singleplay("Pendulum-v1", rl_config, 200 * 40, is_mp=True)

    def test_Pendulum_uvfa(self):
        rl_config = srl.rl.agent57_light.Config(**self.pendulum_config)
        rl_config.input_ext_reward = True
        rl_config.input_int_reward = True
        rl_config.input_action = True
        self.tester.play_verify_singleplay("Pendulum-v1", rl_config, 200 * 100)

    def test_Pendulum_memory(self):
        rl_config = srl.rl.agent57_light.Config(**self.pendulum_config)
        rl_config.memory_name = "ProportionalMemory"
        self.tester.play_verify_singleplay("Pendulum-v1", rl_config, 200 * 50)

    def test_Pendulum_dis_int(self):
        rl_config = srl.rl.agent57_light.Config(**self.pendulum_config)
        rl_config.enable_intrinsic_reward = False
        self.tester.play_verify_singleplay("Pendulum-v1", rl_config, 200 * 70)


if __name__ == "__main__":
    unittest.main(module=__name__, defaultTest="Test.test_Pendulum", verbosity=2)
