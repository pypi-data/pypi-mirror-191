from ray.rllib.env import ParallelPettingZooEnv
from ray.rllib.agents import ppo
from ray.tune import register_env
from ray import tune
from gym import spaces


from gobblet import gobblet_v1

def env_creator(args):
    env = gobblet_v1.parallel_env()
    return env


if __name__ == "__main__":
    env_name = "gobblet_pettingzoo"

    register_env(env_name, lambda config: ParallelPettingZooEnv(env_creator(config)))

    test_env = ParallelPettingZooEnv(env_creator({}))
    obs_space = test_env.observation_space
    obs_space = obs_space["observation"]
    obs_space = spaces.Box(obs_space.low, obs_space.high, obs_space.shape, obs_space.dtype)
    act_space = test_env.action_space
    act_space = spaces.Discrete(act_space.n)

    def gen_policy(i):
        config = {
            "gamma": 0.99,
        }
        return (None, obs_space, act_space, config)


    agents = ["player_1", "player_2"]
    custom_config = {
        "env": env_name,
        "framework": "torch",
        # Use GPUs iff `RLLIB_NUM_GPUS` env var set to > 0.
        # "num_gpus": int(torch.cuda.device_count()),
        "num_gpus": 0,
        "num_workers": 1,  # os.cpu_count() - 1,
        "multiagent": {
            "policies": {
                name: (None, obs_space, act_space, {})
                for name in agents
            },
            "policy_mapping_fn": lambda agent_id: agent_id,
        },
    }

    ppo_config = ppo.DEFAULT_CONFIG.copy()
    ppo_config.update(custom_config)

    trainer = ppo.PPOTrainer(config=ppo_config)

    result = trainer.train()


    policies = {"policy_0": gen_policy(0)}

    policy_ids = list(policies.keys())

    tune.run(
        "PPO",
        name="PPO",
        stop={"timesteps_total": 5000000},
        checkpoint_freq=10,
        local_dir="~/ray_results/"+env_name,
        config={
            # Environment specific
            "env": env_name,
            "no_done_at_end": True,
            "num_gpus": 0,
            "num_workers": 2,
            "num_envs_per_worker": 1,
            "compress_observations": False,
            "batch_mode": 'truncate_episodes',
            "clip_rewards": False,
            "vf_clip_param": 500.0,
            "entropy_coeff": 0.01,
            # effective batch_size: train_batch_size * num_agents_in_each_environment [5, 10]
            # see https://github.com/ray-project/ray/issues/4628
            "train_batch_size": 1000,  # 5000
            "rollout_fragment_length": 50,  # 100
            "sgd_minibatch_size": 100,  # 500
            "vf_share_layers": False
            },
    )