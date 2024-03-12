## What


Motion tracking room heater

- DIY project
- Automatic motion tracking OR remote position adjustment (in browser)
- Three modes for power (650 / 1300 / 2000 W)
- Fun


## How
- Disassemble and rewire an [off-the-shelf heater](https://nl.trotec.com/shop/infrarood-warmtestraler-ir-2000-s.html)
- 3D printed housing, which contains a RPi, [Fisheye camera](https://www.reichelt.nl/nl/nl/raspberry-pi-camera-5mp-160--rpi-wwcam-p148944.html?PROVID=2809&gad_source=1&gclid=Cj0KCQjw-r-vBhC-ARIsAGgUO2DabBkZaEDDHTQ2mxIRW8I1t5CUN7ig8r1uvSDgkZWYHQyTPnTTsTYaAq34EALw_wcB), some relais to switch the heater & TMC2209 stepper driver (using [this](https://pypi.org/project/TMC-2209-Raspberry-Pi/0.1.0/) library) to control the motor.
- The heater swivels horizontally over 180 deg and is actuated by a silent drive stepper motor + belt drive. 
- Set the power and position with a simple interface in your browser. Motion tracking is performed in auto mode.