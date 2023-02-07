import torch
import os
from IPython.display import Image, clear_output  # to display images
print(f"Setup complete. Using torch {torch.__version__} ({torch.cuda.get_device_properties(0).name if torch.cuda.is_available() else 'CPU'})")
from roboflow import Roboflow
rf = Roboflow(model_format="yolov5", notebook="ultralytics")
os.environ["DATASET_DIRECTORY"] = "/content/datasets"
rf = Roboflow(api_key="CsShqMappPKknlP1xlp0")
project = rf.workspace("danish-shukor-5pnil").project("paint-inspection-fingerprint")
dataset = project.version(4).download("yolov5")
#python train.py --img 416 --batch 20 --epochs 150 --data {dataset.location}/data.yaml --weights yolov5s.pt --cache
print(dataset.location)