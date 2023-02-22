#!/usr/bin/env python
# coding: utf-8

# In[8]:


import torchvision
from torchvision.models.detection import FasterRCNN
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from torchvision.models.detection.rpn import AnchorGenerator


def create_model(num_classes):
    
    model = torchvision.models.detection.fasterrcnn_resnet50_fpn(weights="DEFAULT")
    
    in_features = model.roi_heads.box_predictor.cls_score.in_features
    
    model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)
    
    backbone = torchvision.models.mobilenet_v2(weights='DEFAULT').features
    backbone.out_channels = 1280
    anchor_generator = AnchorGenerator(sizes=((32,64,128,256,512),), aspect_ratios=((0.5, 1.0, 2.0),))
    
    roi_pooler = torchvision.ops.MultiScaleRoIAlign(featmap_names=['0'], output_size=7, sampling_ratio=2)

    model = FasterRCNN(backbone, num_classes=num_classes, rpn_anchor_generator=anchor_generator, box_roi_pool=roi_pooler)
    
    return model

