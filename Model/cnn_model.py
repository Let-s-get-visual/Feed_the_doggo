import torch.nn as nn
import torch.nn.functional as F


class CNN(nn.Module):

    def __init__(self):
        super(CNN, self).__init__()
        self.dropout = nn.Dropout2d(0.8)
        self.input = nn.Conv2d(1, 64, 2, 1)
        self.batch1 = nn.BatchNorm2d(64)

        self.conv1 = nn.Conv2d(64, 128, 2, 1)
        self.batch2 = nn.BatchNorm2d(128)

        self.conv2 = nn.Conv2d(128, 256, 2, 1)
        self.batch3 = nn.BatchNorm2d(256)

        self.conv3 = nn.Conv2d(256, 256, 2, 1)
        self.batch4 = nn.BatchNorm2d(256)

        self.max_pool = nn.MaxPool2d(kernel_size=2, stride=2)

        self.fc1 = nn.Linear(256*6*6, 128)
        self.fc2 = nn.Linear(128, 3)

    def forward(self, x):

        x = F.relu(self.batch1(self.input(x)))

        x = F.relu(self.dropout(self.batch2(self.conv1(x))))

        x = self.max_pool(x)

        x = F.relu(self.dropout(self.batch3(self.conv2(x))))

        x = F.relu(self.dropout(self.batch4(self.conv3(x))))

        x = self.max_pool(x)

        x = x.view(-1, 256*6*6)

        x = F.relu(self.dropout(self.fc1(x)))
        x = F.relu(self.fc2(x))

        return x