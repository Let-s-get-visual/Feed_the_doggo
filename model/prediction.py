import torch
import torch.nn.functional as F
from model.cnn_model import CNN

model = CNN()
model.load_state_dict(torch.load("model/modelDict_best_loss.pth", map_location='cpu'))
model.eval()

def predict(image):

    tensor = torch.from_numpy(image).float()
    outputs = model(tensor)
    probs = F.log_softmax(outputs, dim=1)
    pred = torch.argmax(probs, dim=1)

    return pred.item()
