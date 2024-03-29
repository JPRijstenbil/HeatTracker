# Pinouts
EN = 19
STEP = 22
DIR = 27
R1 = 23
R2 = 24

# Actuator settings
TMC_BAUDRATE = 512000
GEARRATIO = 57.0/16.0
MAX_MOTORCURRENT = 1000 # mA
MAX_ACCELERATION = 100 # default 500 
MAX_SPEED = 2000
MICROSTEP = 16
FINETUNE = 1.08
STEPRATIO = (GEARRATIO * MICROSTEP * 200 * FINETUNE) / 360  # steps/rotation

# Camera settings
RESOLUTION = (320, 240)
PIXELCHANGE_THRESHOLD = 0.3 * 255
MOVEMENT_THRESHOLD = 20

# Folders
IMAGEFOLDER = "/home/pi/Documents/heater/images/"
PYTHON_PACKAGES = "/home/pi/.local/lib/python3.7/site-packages"