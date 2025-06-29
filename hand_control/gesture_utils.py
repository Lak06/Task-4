import torch.nn as nn
import torch.nn.functional as F

class GestureNet(nn.Module):
    def __init__(self, input_size=63, num_classes=6):
        super(GestureNet, self).__init__()
        self.fc1 = nn.Linear(input_size, 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, num_classes)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x