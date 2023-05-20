import numpy as np
import pytest

import srl
from srl import runner
from srl.algorithms import ql, ql_agent57
from srl.envs import grid, ox  # noqa F401


def test_train():
    config = runner.Config("OX", ql.Config(), base_dir="tmp_test")
    runner.train(
        config,
        timeout=5,
        eval=runner.EvalOption(),
        progress=runner.ProgressOption(),
        history=runner.HistoryOption(write_memory=True, write_file=True),
        checkpoint=runner.CheckpointOption(
            checkpoint_interval=1,
            eval=runner.EvalOption(),
        ),
    )


def test_train_only():
    rl_config = ql_agent57.Config()
    config = runner.Config("Grid", rl_config)

    _, memory, _ = runner.train(config, max_steps=10_000, disable_trainer=True)

    assert memory.length() > 1000
    rl_config.memory_warmup_size = 1000
    parameter, _, history = runner.train_only(
        config,
        remote_memory=memory,
        max_train_count=50_000,
        eval=runner.EvalOption(),
        progress=runner.ProgressOption(),
        history=runner.HistoryOption(write_memory=True, write_file=True),
        checkpoint=runner.CheckpointOption(
            checkpoint_interval=1,
            eval=runner.EvalOption(),
        ),
    )
    # history.plot()

    rewards = runner.evaluate(config, parameter, max_episodes=100)
    reward = np.mean(rewards)
    assert reward > 0.5, f"reward: {reward}"


def test_render():
    pytest.importorskip("cv2")
    pytest.importorskip("matplotlib")
    pytest.importorskip("PIL")
    pytest.importorskip("pygame")

    env_config = srl.EnvConfig("Grid")
    rl_config = ql.Config()
    config = runner.Config(env_config, rl_config)

    # train
    parameter, _, _ = runner.train(config, max_steps=10000)

    # eval
    rewards = runner.evaluate(config, parameter, max_episodes=100)
    rewards = np.mean(rewards)
    print(rewards)
    assert rewards > 0.5

    # render terminal
    rewards = runner.render(config, parameter)
    rewards = np.mean(rewards)
    print(rewards)
    assert rewards > 0.5

    # render window
    rewards = runner.render_window(config, parameter)
    rewards = np.mean(rewards)
    print(rewards)
    assert rewards > 0.5

    # animation
    render = runner.animation(config, parameter)
    rewards = np.mean(rewards)
    print(rewards)
    assert rewards > 0.5

    render.create_anime()


def test_play():
    pytest.importorskip("cv2")
    pytest.importorskip("matplotlib")
    pytest.importorskip("PIL")
    pytest.importorskip("pygame")

    config = runner.Config(srl.EnvConfig("Grid"), None)
    render = runner.animation(config, max_steps=10)
    render.create_anime(draw_info=True).save("tmp_test/a.gif")

    config = runner.Config(srl.EnvConfig("Grid"), None)
    render = runner.animation(config, max_steps=10)
    render.create_anime(draw_info=True).save("tmp_test/b.gif")


def test_gym():
    pytest.importorskip("cv2")
    pytest.importorskip("matplotlib")
    pytest.importorskip("PIL")
    pytest.importorskip("pygame")
    pytest.importorskip("gym")

    config = runner.Config(srl.EnvConfig("MountainCar-v0"), None)
    render = runner.animation(config, max_steps=10)
    render.create_anime(draw_info=True).save("tmp_test/c.gif")

    config = runner.Config(srl.EnvConfig("MountainCar-v0"), None)
    render = runner.animation(config, max_steps=10)
    render.create_anime(draw_info=True).save("tmp_test/d.gif")


def test_shuffle_player():
    env_config = srl.EnvConfig("OX")
    config = runner.Config(env_config, None, seed=1)
    config.players = ["cpu", "random"]

    # shuffle した状態でも報酬は元の順序を継続する
    rewards = runner.evaluate(config, parameter=None, max_episodes=100, shuffle_player=True)
    rewards = np.mean(rewards, axis=0)
    assert rewards[0] > 0.7  # CPUがまず勝つ
