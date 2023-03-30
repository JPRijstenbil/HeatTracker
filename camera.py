import picamera
import numpy as np
import time

IMAGEFOLDER = "/home/pi/Documents/heater/images/"

with picamera.PiCamera() as camera:
    # camera.exposure_mode = 'auto'
    # camera.exposure_compensation = 0
    # camera.shutter_speed = int(6 * 10**-6)  # 0.1 s = 10fps, good enough lighting even in evening
    # camera.iso = 800
    # camera.start_preview()
    camera.resolution = (320, 240)
    # camera.awb_mode = 'auto'  # Automatic white balance
    
    camera.shutter_speed = 0
    camera.iso = 0
    camera.rotation = 180

    time.sleep(2)
    camera.exposure_mode = 'auto'  # Manual exposure mode
    time.sleep(2)
    t = time.time()
    camera.capture(IMAGEFOLDER + 'image.jpg')
    print("elapsed ", t - time.time())



