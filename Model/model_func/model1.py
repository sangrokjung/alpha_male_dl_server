import torch
import torchvision
import numpy as np
import glob as glob
import cv2
import argparse
import sys
import os


from pathlib import Path
from model import create_model


FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
num_classes = 2
CLASSES = ['background','face']

def run(weights=ROOT / 'alphav1.pth',
       source=ROOT / 'data/image',
       conf_thres=0.8):
    
    weights = str(weights)
    source = str(source)
    conf_thres = float(conf_thres)
    model = create_model(num_classes).to(DEVICE)
    model.load_state_dict(torch.load(weights, map_location=DEVICE))
    model.eval()
    test_image = glob.glob(f"{source}/*")
    image_name = test_image[0].split('/')[-1].split('.')[0]
    image = cv2.imread(test_image[0])
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
        return print(1)
    else:
        return print(0)
    
    
def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', nargs='+', type=str, default=ROOT / 'alphav1.pth', help='model path')
    parser.add_argument('--source', type=str, default=ROOT / 'data/image', help='filepath that you want to predict')
    parser.add_argument('--conf-thres', type=float, default=0.7, help='confidence threshold')
    opt = parser.parse_args()
    return opt


def main(opt):
    run(**vars(opt))

    
if __name__ == "__main__":
    opt = parse_opt()
    main(opt)

