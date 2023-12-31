import logging
from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Tuple

import numpy as np

from srl.base.define import EnvObservationTypes, InfoType, RLActionType, RLObservationType, RLTypes
from srl.base.env.env_run import EnvRun, SpaceBase
from srl.base.rl.base import RLConfig
from srl.base.rl.worker_rl import RLWorker
from srl.base.rl.worker_run import WorkerRun

logger = logging.getLogger(__name__)


@dataclass
class DiscreteActionConfig(RLConfig):
    @property
    def action_type(self) -> RLTypes:
        return RLTypes.DISCRETE

    def set_config_by_env(
        self,
        env: EnvRun,
        env_action_space: SpaceBase,
        env_observation_space: SpaceBase,
        env_observation_type: EnvObservationTypes,
    ) -> None:
        self._action_num = env_action_space.n

    @property
    def action_num(self) -> int:
        return self._action_num


class DiscreteActionWorker(RLWorker):
    @abstractmethod
    def call_on_reset(
        self,
        state: np.ndarray,
        invalid_actions: List[int],
    ) -> InfoType:
        raise NotImplementedError()

    @abstractmethod
    def call_policy(
        self,
        state: np.ndarray,
        invalid_actions: List[int],
    ) -> Tuple[int, InfoType]:
        raise NotImplementedError()

    @abstractmethod
    def call_on_step(
        self,
        next_state: np.ndarray,
        reward: float,
        done: bool,
        next_invalid_actions: List[int],
    ) -> InfoType:
        raise NotImplementedError()

    # --------------------------------------

    def _call_on_reset(self, state: RLObservationType, env: EnvRun, worker: WorkerRun) -> InfoType:
        return self.call_on_reset(state, self.get_invalid_actions())

    def _call_policy(self, state: RLObservationType, env: EnvRun, worker: WorkerRun) -> Tuple[RLActionType, InfoType]:
        return self.call_policy(state, self.get_invalid_actions())

    def _call_on_step(
        self,
        next_state: RLObservationType,
        reward: float,
        done: bool,
        env: EnvRun,
        worker: WorkerRun,
    ) -> InfoType:
        return self.call_on_step(next_state, reward, done, self.get_invalid_actions())
