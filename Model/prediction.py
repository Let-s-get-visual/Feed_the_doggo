import torch
import torch.nn.functional as F
from cnn_model import CNN

model = CNN()

model.load_state_dict(torch.load("modelDict_best_loss.pth", map_location='cpu'))

model.eval()


def predict(image):

    tensor = torch.from_numpy(image).float()
    outputs = model(tensor)
    probs = F.log_softmax(outputs)
    print(probs)
    pred = torch.argmax(probs, dim=1)
    print(pred)

    return pred.item()
