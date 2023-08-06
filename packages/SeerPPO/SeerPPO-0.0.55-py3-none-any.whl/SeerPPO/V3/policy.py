import torch
from torch import nn

from SeerPPO.distribution import CategoricalDistribution


class SeerNetworkV3(nn.Module):
    def __init__(self):
        super().__init__()

        self.activation = nn.LeakyReLU(inplace=True)

        self.OBS_SIZE = 142

        self.ENCODER_INTERMEDIATE_SIZE = 1024

        self.encoder = nn.Sequential(
            nn.Linear(self.OBS_SIZE, self.ENCODER_INTERMEDIATE_SIZE),
            self.activation,
            nn.Linear(self.ENCODER_INTERMEDIATE_SIZE, self.ENCODER_INTERMEDIATE_SIZE),
            self.activation,
            nn.Linear(self.ENCODER_INTERMEDIATE_SIZE, self.ENCODER_INTERMEDIATE_SIZE),
            self.activation,
            nn.Linear(self.ENCODER_INTERMEDIATE_SIZE, self.ENCODER_INTERMEDIATE_SIZE),
            self.activation,
        )

        self.value_network = nn.Sequential(
            nn.Linear(self.ENCODER_INTERMEDIATE_SIZE, self.ENCODER_INTERMEDIATE_SIZE // 2),
            self.activation,
            nn.Linear(self.ENCODER_INTERMEDIATE_SIZE // 2, self.ENCODER_INTERMEDIATE_SIZE // 2),
            self.activation,
            nn.Linear(self.ENCODER_INTERMEDIATE_SIZE // 2, self.ENCODER_INTERMEDIATE_SIZE // 2),
            self.activation,
            nn.Linear(self.ENCODER_INTERMEDIATE_SIZE // 2, 1),
        )

        self.policy_network = nn.Sequential(
            nn.Linear(self.ENCODER_INTERMEDIATE_SIZE, self.ENCODER_INTERMEDIATE_SIZE // 2),
            self.activation,
            nn.Linear(self.ENCODER_INTERMEDIATE_SIZE // 2, self.ENCODER_INTERMEDIATE_SIZE // 2),
            self.activation,
            nn.Linear(self.ENCODER_INTERMEDIATE_SIZE // 2, self.ENCODER_INTERMEDIATE_SIZE // 2),
            self.activation,
            nn.Linear(self.ENCODER_INTERMEDIATE_SIZE // 2, 90),
        )

        self.distribution = CategoricalDistribution(90)
        self.HUGE_NEG = None
        self.ones = None
        self.jump_mask = None
        self.boost_mask = None
        self.pitch_roll_mask = None
        self.handbrake_mask = None

    def encode(self, obs):

        assert obs.shape[-1] in [142]

        if obs.shape[-1] == 142:
            return self.encoder(obs)

    def forward(self, obs, deterministic):

        if self.HUGE_NEG is None:
            self.HUGE_NEG = torch.tensor(-1e8, dtype=torch.float32).to(obs.device)

        # Rollout
        x = self.encode(obs)

        value = self.value_network(x)
        policy_logits = self.policy_network(x)
        mask = self.create_mask(obs)
        policy_logits = torch.where(mask, policy_logits, self.HUGE_NEG)
        self.distribution.proba_distribution(policy_logits)
        self.distribution.apply_mask(mask)

        actions = self.distribution.get_actions(deterministic=deterministic)
        log_prob = self.distribution.log_prob(actions)
        return actions, value, log_prob,

    def predict_value(self, obs):
        # Rollout
        x = self.encode(obs)
        value = self.value_network(x)
        return value

    def predict_actions(self, obs, deterministic):
        if self.HUGE_NEG is None:
            self.HUGE_NEG = torch.tensor(-1e8, dtype=torch.float32).to(obs.device)

            # Rollout
        x = self.encode(obs)

        policy_logits = self.policy_network(x)
        mask = self.create_mask(obs)
        policy_logits = torch.where(mask, policy_logits, self.HUGE_NEG)
        self.distribution.proba_distribution(policy_logits)
        self.distribution.apply_mask(mask)

        actions = self.distribution.get_actions(deterministic=deterministic)
        return actions

    def evaluate_actions(self, obs, actions, mask):

        if self.HUGE_NEG is None:
            self.HUGE_NEG = torch.tensor(-1e8, dtype=torch.float32).to(obs.device)

        x = self.encode(obs)

        value = self.value_network(x)
        policy_logits = self.policy_network(x)
        policy_logits = torch.where(mask, policy_logits, self.HUGE_NEG)
        self.distribution.proba_distribution(policy_logits)
        log_prob = self.distribution.log_prob(actions)

        entropy = self.distribution.entropy()

        return value, log_prob, entropy

    def create_mask(self, obs):

        has_boost = obs[:, 13] > 0.0
        on_ground = obs[:, 14] == 1
        has_flip = obs[:, 15] == 1
        in_air = torch.logical_not(on_ground)

        if self.ones is None:
            self.ones = torch.ones(1, dtype=torch.bool, device=obs.device, requires_grad=False)

        if self.jump_mask is None:
            self.jump_mask = torch.tensor([1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
                                           1., 1., 1., 1., 1., 1., 1., 1., 0., 0., 1., 1., 0., 0., 1., 1., 0., 0., 1., 1., 1., 1., 1., 1.,
                                           1., 1., 1., 1., 1., 1., 0., 0., 0., 0., 1., 1., 0., 0., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
                                           1., 1., 0., 0., 1., 1., 0., 0., 1., 1., 0., 0., 1., 1., 1., 1., 1., 1.], dtype=torch.bool, device=obs.device, requires_grad=False)

        if self.boost_mask is None:
            self.boost_mask = torch.tensor([1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 0., 0., 1., 1., 0., 0., 1., 1., 0., 0.,
                                            1., 0., 1., 0., 1., 0., 1., 0., 1., 0., 1., 0., 1., 0., 1., 0., 1., 0., 1., 0., 1., 0., 1., 0.,
                                            1., 0., 1., 0., 1., 0., 1., 0., 1., 0., 1., 0., 1., 0., 1., 0., 1., 0., 1., 0., 1., 0., 1., 0.,
                                            1., 0., 1., 0., 1., 0., 1., 0., 1., 0., 1., 0., 1., 0., 1., 0., 1., 0.], dtype=torch.bool, device=obs.device, requires_grad=False)

        if self.pitch_roll_mask is None:
            self.pitch_roll_mask = torch.tensor([1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
                                                 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
                                                 0., 0., 0., 0., 0., 0., 0., 0., 1., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
                                                 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.], dtype=torch.bool, device=obs.device, requires_grad=False)

        if self.handbrake_mask is None:
            self.handbrake_mask = torch.tensor([1., 0., 1., 0., 1., 0., 1., 0., 1., 0., 1., 0., 1., 0., 1., 0., 1., 0., 1., 0., 1., 0., 1., 0.,
                                                1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
                                                1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
                                                1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.], dtype=torch.bool, device=obs.device, requires_grad=False)

        with torch.no_grad():

            mask_0 = torch.where(has_boost.unsqueeze(1), self.ones, self.boost_mask)
            mask_1 = torch.where(has_flip.unsqueeze(1), self.ones, self.jump_mask)
            mask_2 = torch.where(in_air.unsqueeze(1), self.ones, self.pitch_roll_mask)
            mask_3 = torch.where(on_ground.unsqueeze(1), self.ones, self.handbrake_mask)

            res = (mask_0 * mask_1) * (mask_2 * mask_3)

        return res


if __name__ == '__main__':
    n = SeerNetworkV3()

    print(n)

    torch.save(n.state_dict(), "./0.pt")

    pytorch_total_params = sum(p.numel() for p in n.parameters())

    print(pytorch_total_params)
