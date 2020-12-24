import numpy as np
import cv2
import time

 class CaptureManager(object):
     def __init__(self,capture,previewWindowManager=None,
     shouldMirrorPreview=False):
     