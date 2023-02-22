import torch
import torch
import numpy as np
import cv2
import base64
from PIL import Image
import io


from Model.model_func.model import create_model



def model1(img, weights):
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    model = create_model(num_classes=2).to(torch.device(DEVICE))
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
    image = np.transpose(image, (2,0,1)).astype(np.float32)
    image = torch.tensor(image, dtype=torch.float).to(DEVICE)
    image = torch.unsqueeze(image, 0)
    with torch.no_grad():
        outputs = model(image)
        
    outputs = [{k:v.to(DEVICE) for k,v in t.items()} for t in outputs]
    if len(outputs[0]['boxes']) != 0:
        return 1
    else:
        return 0

