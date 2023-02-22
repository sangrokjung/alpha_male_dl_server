

import sys
sys.path.extend("./")
from Model.model_func.alpha1 import model1
from Model.model_func.alpha3 import model3

def run(img):
    model1_result = model1(img=img, weights="Model/model_1.pth")
    if model1_result == 0:
        return 0
    if model1_result == 1:
        return model3(img=img, weights="Model/model_3.pth")

