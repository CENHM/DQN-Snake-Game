import random
import time
import torch
import torch.nn as nn
from GameGUI import SnakeGameGUI
from utils import ACTION


def main():
    tensor1 = torch.rand(5, 3).max(1)[0]
    tensor2 = torch.rand(5)
    tensor3 = nn.MSELoss()(tensor1, tensor2)
    pass

if __name__ == "__main__":
    main()
