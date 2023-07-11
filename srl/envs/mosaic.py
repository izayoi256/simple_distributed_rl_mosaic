import logging
import pickle
from dataclasses import dataclass
from typing import Any, Tuple

import numpy as np

from srl.base.define import EnvActionType, EnvObservationTypes, InvalidActionsType
from srl.base.env.genre import TurnBase2Player
from srl.base.env.registration import register
from srl.base.spaces import BoxSpace, DiscreteSpace

from srl.envs.mosaic_core import Game
logger = logging.getLogger(__name__)

register(
    id="Mosaic",
    entry_point=__name__ + ":Mosaic",
    kwargs={"size": 7},
)
register(
    id="Mosaic7",
    entry_point=__name__ + ":Mosaic",
    kwargs={"size": 7},
)
register(
    id="Mosaic5",
    entry_point=__name__ + ":Mosaic",
    kwargs={"size": 5},
)
register(
    id="Mosaic3",
    entry_point=__name__ + ":Mosaic",
    kwargs={"size": 3},
)


@dataclass
class Mosaic(TurnBase2Player):
    size: int = 7

    def __post_init__(self):
        self.game = None
        self.actions_n = sum([i * i for i in range(1, self.size + 1)])
        self.actions = [i for i in range(self.actions_n)]

    @property
    def action_space(self) -> DiscreteSpace:
        return DiscreteSpace(self.actions_n)

    @property
    def observation_space(self) -> BoxSpace:
        return BoxSpace(shape=(self.size, self.size, self.size), low=0, high=1)

    @property
    def observation_type(self) -> EnvObservationTypes:
        return EnvObservationTypes.SHAPE3

    @property
    def max_episode_steps(self) -> int:
        return sum([i * i for i in range(1, self.size + 1)]) - 1

    @property
    def next_player_index(self) -> int:
        return 0 if self.game.is_first_turn else 1

    def call_reset(self) -> Tuple[np.ndarray, dict]:
        self.game = Game(self.size)
        return self.observe(), self.additional_info()

    def observe(self) -> np.ndarray:
        first_board = self.observe_single_board(self.size, self.game.first_board)
        second_board = self.observe_single_board(self.size, self.game.second_board)
        legal_board = self.observe_single_board(self.size, self.game.legal_board)
        result = legal_board - 1
        result[first_board == 1] = 1
        result[second_board == 2] = 2
        return result

    def additional_info(self) -> dict:
        return {
            "first": f"{self.game.first_score}/{self.game.pieces_per_player}",
            "second": f"{self.game.second_score}/{self.game.pieces_per_player}",
        }

    def backup(self) -> Any:
        return pickle.dumps(
            [
                self.size,
                list(self.game.moves),
            ]
        )

    def restore(self, data: Any) -> None:
        d = pickle.loads(data)
        self.size = d[0]
        self.game = Game(self.size)
        for move in d[1]:
            self.game.make_move(move)

    def call_step(self, action: EnvActionType) -> Tuple[np.ndarray, float, float, bool, dict]:

        self.game.make_move(action)

        if self.game.is_over:
            if self.game.first_wins:
                reward1 = 1
            elif self.game.second_wins:
                reward1 = -1
            else:
                reward1 = 0

            reward2 = reward1 * -1
            done = True
        else:
            reward1 = reward2 = 0
            done = False

        return self.observe(), reward1, reward2, done, self.additional_info()

    def get_invalid_actions(self, player_index: int = -1) -> InvalidActionsType:
        legal_moves = list(self.game.legal_moves)
        return [i for i in self.actions if i not in legal_moves]

    def render_terminal(self, **kwargs) -> None:
        first_board = list(self.game.first_board)
        second_board = list(self.game.second_board)
        neutral_board = list(self.game.neutral_board)
        legal_board = list(self.game.legal_board)
        last_move = self.game.last_move
        i = 0
        for y in range(self.size):
            print("-" + "----" * (y + 1))
            for z in range(y+1):
                print(f"|", end="")
                for x in range(y+1):
                    i -= 1
                    action = (i * -1) - 1

                    if legal_board[i] == "1":
                        print(str(action).rjust(3, " ") + "|", end="")
                        continue

                    if first_board[i] == "1":
                        char = "O"
                    elif second_board[i] == "1":
                        char = "X"
                    elif neutral_board[i] == "1":
                        char = "@"
                    else:
                        char = " "

                    cell = f" {char} " if last_move is None or last_move != action else f">{char} "
                    print(cell + "|", end="")
                print()
            print("-" + "----" * (y + 1))

    @staticmethod
    def observe_single_board(size: int, board: str):
        result = np.zeros((size, size, size), dtype=np.uint8)
        reversed_board = "".join(list(reversed(board)))
        for layer_index in (range(0, size)):
            layer_size = layer_index + 1
            start = sum(i ** 2 for i in range(layer_size))
            end = start + layer_size ** 2
            layer = np.array(list(reversed_board[start:end]), dtype=np.uint8).reshape([layer_size, layer_size])
            result[layer_index][:layer_size, :layer_size] = layer
        return result

    @property
    def render_interval(self) -> float:
        return 1500 / 2
