import torch
import torchvision
import numpy as np
import cv2
import base64
from PIL import Image
import io

from Model.model_func.model import create_model


def model3(img, weights):
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    model = create_model(num_classes=16).to(torch.device(DEVICE))
    model.load_state_dict(torch.load(weights, map_location=DEVICE))
    model.eval()
    decoded_img = base64.b64decode(img)
    img_out = Image.open(io.BytesIO(decoded_img))
    img_numpy_array = np.array(img_out)
    image = cv2.cvtColor(img_numpy_array, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (178, 218))
    orig_image = image.copy()
    image = cv2.cvtColor(orig_image, cv2.COLOR_BGR2RGB).astype(np.float32)
    image /= 255.0
    image = np.transpose(image, (2, 0, 1)).astype(np.float32)
    image = torch.tensor(image, dtype=torch.float).to(DEVICE)
    image = torch.unsqueeze(image, 0)
    with torch.no_grad():
        outputs = model(image)

    outputs = [{k: v.to(DEVICE) for k, v in t.items()} for t in outputs]

    if len(outputs[0]['boxes']) != 0:
        scores = outputs[0]['scores'].data.numpy()
        labels = outputs[0]['labels'].cpu().numpy()
        labels = list(labels[scores >= 0.75])

        if len(labels) == 3:
            if 1 in labels or 4 in labels or 7 in labels or 10 in labels or 13 in labels:
                if 2 in labels or 5 in labels or 8 in labels or 11 in labels or 14 in labels:
                    if 3 in labels or 6 in labels or 9 in labels or 12 in labels or 15 in labels:
                        score = 0
                        for i in range(len(labels)):
                            if labels[i] == 1:
                                score += 50
                            elif labels[i] == 2:
                                score += 40
                            elif labels[i] == 3:
                                score += 10
                            elif labels[i] == 4:
                                score += 40
                            elif labels[i] == 5:
                                score += 32
                            elif labels[i] == 6:
                                score += 8
                            elif labels[i] == 7:
                                score += 30
                            elif labels[i] == 8:
                                score += 24
                            elif labels[i] == 9:
                                score += 6
                            elif labels[i] == 10:
                                score += 20
                            elif labels[i] == 11:
                                score += 16
                            elif labels[i] == 12:
                                score += 4
                            elif labels[i] == 13:
                                score += 10
                            elif labels[i] == 14:
                                score += 8
                            elif labels[i] == 15:
                                score += 2

                        if score > 85:
                            cls = 1
                        elif score > 68:
                            cls = 2
                        elif score > 48:
                            cls = 3
                        elif score > 20:
                            cls = 4
                        elif score > 0:
                            cls = 5

                        return cls
        if len(labels) != 3:
            return 6

