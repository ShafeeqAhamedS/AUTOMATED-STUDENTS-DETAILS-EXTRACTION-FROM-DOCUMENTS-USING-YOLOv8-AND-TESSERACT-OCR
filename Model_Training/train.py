from ultralytics import YOLO
from IPython.display import display, Image
import os

HOME = ''
!yolo task=detect mode=train model=yolov8s.pt data={HOME}/dataset/data.yaml epochs=100 imgsz=800 plots=True