# TelloTV
TelloTV is a rather simplistic approach to be able to launch your Tello drone & have it track your face. This approach has been tested & proven to work with the DJI Tello Drone (Non - Educational Version I believe, but may still work with the educational version?)

Tested with Python 3.6, but it also may be compatabile with other versions.

## Example
https://youtu.be/esw88_gKOpA

## Install
```
$ pip install -r requirements.txt
```

## Usage
```
  -h, --help            ** = required
  -d DISTANCE, --distance DISTANCE
                        use -d to change the distance of the drone. Range 0-6
                        (default: 3)
  -sx SAFTEY_X, --saftey_x SAFTEY_X
                        use -sx to change the saftey bound on the x axis .
                        Range 0-480 (default: 100)
  -sy SAFTEY_Y, --saftey_y SAFTEY_Y
                        use -sy to change the saftey bound on the y axis .
                        Range 0-360 (default: 55)
  -os OVERRIDE_SPEED, --override_speed OVERRIDE_SPEED
                        use -os to change override speed. Range 0-3 (default:
                        1)
  -ss, --save_session   add the -ss flag to save your session as an image
                        sequence in the Sessions folder (default: False)
  -D, --debug           add the -D flag to enable debug mode. Everything works
                        the same, but no commands will be sent to the drone
                        (default: False)
```

## Controls
- Esc: Quit Application
- T: Takeoff
- L: To Land

##### AI Mode
- 0: Set Drone distance to 0
- 1: Set Drone distance to 1
- 2: Set Drone distance to 2
- 3: Set Drone distance to 3
- 4: Set Drone distance to 4
- 5: Set Drone distance to 5
- 6: Set Drone distance to 6

##### Override Mode
- Backspace: Enable / Disable Override mode
- W/S: Fly Forward/Back
- A/D: Pan Left/Right
- Q/E: Fly Up/Down
- Z/C: Fly Left/Right
- 1: Set Drone speed to 1
- 2: Set Drone speed to 2
- 3: Set Drone speed to 3

## Research Notes
- 02.19.019 - This has been tested outside, & it appears that there is too much happening in most outdoor public spaces. Seeing as the Tello has no internal storage & needs to send each video frame to a computer via WiFi, many things can go wrong in the process, but from what I observed the biggest issues appear to be: The Computer to Tello communication can be met with WiFi interference, delivering data at an unsustainable rate. The image data can become corrupted, making faces unrecognizable for OpenCV to process from, thus reducing the accuracy of the algorithm. In addition, the Tello is rather light, so if there is a lot of wind, it will be difficult to sit still, & in cases where it can, it may be slightly tilted, again making faces hard for the OpenCV algorithm to detect. 

## Roadmap
- Figure out a way to save images at a frame rate from 24-60, or at least 12 fps
- Display current battery power on screen
- Add a movement gradient dependent on distance from subject
- Add more to the facial recog to be able to tell when the drone needs to fly left or right
- Use pose estimation for input commands
- Add a function where the drone will ignore all faces except the one you specify
- ~~Fix key pressing spam~~

# Credits
This script has been adapted from Damià Fuentes Escoté's [TelloSDKPy](https://github.com/damiafuentes/DJITelloPy) script, please check it out if you want to learn more about that.

#### AI
- **Jabrils**

#### Backend Thanks
- **Damià Fuentes Escoté** 
