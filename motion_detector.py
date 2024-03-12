## IMPORTS
import io
import queue
import time
import picamera
import numpy as np
from PIL import Image
import settings

class MotionDetector(io.BytesIO):
    def __init__(self):
        super().__init__()
        empty_img = np.zeros((settings.RESOLUTION[1], settings.RESOLUTION[0], 3)).astype('uint8')
        self.current_frame = empty_img
        self.last_frame = empty_img
        self.diff = empty_img
        self.camera = picamera.PiCamera()
        self.init_camera()
        self.q = queue.Queue()

    def run(self, cond, shared_data):
        try:
            self.camera.start_recording(self, format='mjpeg', quality=30)
            self.camera.wait_recording(100)
        except:
            self.camera.stop_recording()

    def write(self, buf):
        self.current_frame = np.array(Image.open(io.BytesIO(buf)))
        self.detect()
        self.last_frame = self.current_frame
        
    def detect(self):
        last_frame_int16 = self.last_frame.astype(np.int16)
        current_frame_int16 = self.current_frame.astype(np.int16)
        self.diff = np.absolute(last_frame_int16 - current_frame_int16).astype('uint8')
        
        y, x = np.where(self.diff[:,:,0] >= settings.PIXELCHANGE_THRESHOLD)

        if y.shape[0] > settings.MOVEMENT_THRESHOLD:
            coords = (int(y.mean()), int(x.mean()))
            self.q.put(coords)
        return
    
    def init_camera(self):
        self.camera.resolution = settings.RESOLUTION
        self.camera.framerate = 2
        self.camera.rotation = 180
        time.sleep(1) 

    def capture_testimage(self):
        self.camera.capture(settings.IMAGEFOLDER + 'testimage.jpg')
