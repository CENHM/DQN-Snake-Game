import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from utils import EPSILON, N_ACTIONS


BATCH_SIZE = 32                                 # 样本数量
LR = 0.5                                       # 学习率
GAMMA = 0.9                                     # reward discount
TARGET_REPLACE_ITER = 5                      # 目标网络更新频率
MEMORY_CAPACITY = 200


class ResNet(nn.Module):
    def __init__(self):
        super(ResNet, self).__init__()
        self.model0 = nn.Sequential(
            nn.Conv2d(in_channels=3, out_channels=64, kernel_size=(7, 7), stride=2, padding=3),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=(3, 3), stride=2, padding=1),
        )
        self.model1 = nn.Sequential(
            nn.Conv2d(in_channels=64, out_channels=64, kernel_size=(3, 3), stride=1, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.Conv2d(in_channels=64, out_channels=64, kernel_size=(3, 3), stride=1, padding=1),
            nn.BatchNorm2d(64),
        )

        self.model2 = nn.Sequential(
            # 1.2
            nn.Conv2d(in_channels=64, out_channels=64, kernel_size=(3, 3), stride=1, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.Conv2d(in_channels=64, out_channels=64, kernel_size=(3, 3), stride=1, padding=1),
            nn.BatchNorm2d(64),
        )

        self.model3 = nn.Sequential(
            # 2.1
            nn.Conv2d(in_channels=64, out_channels=128, kernel_size=(3, 3), stride=2, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.Conv2d(in_channels=128, out_channels=128, kernel_size=(3, 3), stride=1, padding=1),
            nn.BatchNorm2d(128),
        )

        self.en1 = nn.Sequential(
            nn.Conv2d(in_channels=64, out_channels=128, kernel_size=(1, 1), stride=2, padding=0),
            nn.BatchNorm2d(128),
            nn.ReLU(),
        )

        self.model4 = nn.Sequential(
            # 2.2
            nn.Conv2d(in_channels=128, out_channels=128, kernel_size=(3, 3), stride=1, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.Conv2d(in_channels=128, out_channels=128, kernel_size=(3, 3), stride=1, padding=1),
            nn.BatchNorm2d(128),
        )

        self.model5 = nn.Sequential(
            # 3.1
            nn.Conv2d(in_channels=128, out_channels=256, kernel_size=(3, 3), stride=2, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(),
            nn.Conv2d(in_channels=256, out_channels=256, kernel_size=(3, 3), stride=1, padding=1),
            nn.BatchNorm2d(256),
        )

        self.en2 = nn.Sequential(
            nn.Conv2d(in_channels=128, out_channels=256, kernel_size=(1, 1), stride=2, padding=0),
            nn.BatchNorm2d(256),
            nn.ReLU(),
        )

        self.model6 = nn.Sequential(
            # 3.2
            nn.Conv2d(in_channels=256, out_channels=256, kernel_size=(3, 3), stride=1, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(),
            nn.Conv2d(in_channels=256, out_channels=256, kernel_size=(3, 3), stride=1, padding=1),
            nn.BatchNorm2d(256),
        )

        self.model7 = nn.Sequential(
            # 4.1
            nn.Conv2d(in_channels=256, out_channels=512, kernel_size=(3, 3), stride=2, padding=1),
            nn.BatchNorm2d(512),
            nn.ReLU(),
            nn.Conv2d(in_channels=512, out_channels=512, kernel_size=(3, 3), stride=1, padding=1),
            nn.BatchNorm2d(512),
        )

        self.en3 = nn.Sequential(
            nn.Conv2d(in_channels=256, out_channels=512, kernel_size=(1, 1), stride=2, padding=0),
            nn.BatchNorm2d(512),
            nn.ReLU(),
        )

        self.model8 = nn.Sequential(
            # 4.2
            nn.Conv2d(in_channels=512, out_channels=512, kernel_size=(3, 3), stride=1, padding=1),
            nn.BatchNorm2d(512),
            nn.ReLU(),
            nn.Conv2d(in_channels=512, out_channels=512, kernel_size=(3, 3), stride=1, padding=1),
            nn.BatchNorm2d(512),
        )

        # AAP 自适应平均池化
        self.aap = nn.AdaptiveAvgPool2d((1, 1))
        # flatten 维度展平
        self.flatten = nn.Flatten(start_dim=1)
        # FC 全连接层
        self.fc = nn.Linear(512, N_ACTIONS)

    def forward(self, x):
        # x = x.transpose(2, 0, 1)

        x = self.model0(x)

        f1 = x
        x = self.model1(x)
        x = x + f1
        x = F.relu(x)

        f1_1 = x
        x = self.model2(x)
        x = x + f1_1
        x = F.relu(x)

        f2_1 = x
        f2_1 = self.en1(f2_1)
        x = self.model3(x)
        x = x + f2_1
        x = F.relu(x)

        f2_2 = x
        x = self.model4(x)
        x = x + f2_2
        x = F.relu(x)

        f3_1 = x
        f3_1 = self.en2(f3_1)
        x = self.model5(x)
        x = x + f3_1
        x = F.relu(x)

        f3_2 = x
        x = self.model6(x)
        x = x + f3_2
        x = F.relu(x)

        f4_1 = x
        f4_1 = self.en3(f4_1)
        x = self.model7(x)
        x = x + f4_1
        x = F.relu(x)

        f4_2 = x
        x = self.model8(x)
        x = x + f4_2
        x = F.relu(x)

        x = self.aap(x)
        x = self.flatten(x)
        x = self.fc(x)
        return x


class DQN(object):
    def __init__(self):
        self.eval_net, self.target_net = ResNet(), ResNet()
        self.target_net.load_state_dict(self.eval_net.state_dict())
        self.learn_step_counter = 0
        self.memory_counter = 0

        self.memory_s, self.memory_a, self.memory_r, self.memory_s_next = [], [], [], []

        self.optimizer = torch.optim.Adam(self.eval_net.parameters(), lr=LR)

    # e-greedy
    def choose_action(self, x):
        if np.random.uniform() < EPSILON:
            actions_value = self.eval_net.forward(x)
            action = torch.max(actions_value, 1)[1].data.numpy()[0]
        else:
            action = np.random.randint(0, N_ACTIONS - 1)
        return action

    # store transition (ϕ_t, a_t, r_t, ϕ_{t+1})
    def store_transition(self, s, a, r, s_):
        if self.memory_counter >= MEMORY_CAPACITY:
            self.memory_s.pop(0)
            self.memory_a.pop(0)
            self.memory_r.pop(0)
            self.memory_s_next.pop(0)
        self.memory_s.append(s)
        self.memory_a.append(a)
        self.memory_r.append(r)
        self.memory_s_next.append(s_)
        self.memory_counter += 1

    def check_learn(self):
        if self.memory_counter % MEMORY_CAPACITY == MEMORY_CAPACITY - 1:
            self.learn()

    def learn(self):
        # sample random minibatch of transition from memory
        sample_index = np.random.choice(MEMORY_CAPACITY, BATCH_SIZE)

        selected_s = torch.FloatTensor([torch.squeeze(self.memory_s[index], 0).numpy() for index in sample_index])
        selected_a = torch.LongTensor([self.memory_a[index] for index in sample_index])
        selected_r = torch.FloatTensor([self.memory_r[index] for index in sample_index])
        selected_s_next = torch.FloatTensor([torch.squeeze(self.memory_s[index], 0).numpy() for index in sample_index])

        q_eval = self.eval_net(selected_s)
        q_eval = q_eval.gather(1, selected_a.unsqueeze(1))
        q_next = self.target_net(selected_s_next).detach()
        q_target = selected_r + GAMMA * q_next.max(1)[0]

        loss = nn.MSELoss()(q_eval, q_target)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        self.learn_step_counter += 1
        # every TARGET_REPLACE_ITER steps reset \hat{Q} = Q
        if self.learn_step_counter % TARGET_REPLACE_ITER == 0:
            self.target_net.load_state_dict(self.eval_net.state_dict())

