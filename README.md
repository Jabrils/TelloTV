# TelloTV
TelloTV is a rather simplistic approach to be able to launch your Tello drone & hav it track your face. This approach has been tested & proven to work with the DJI Tello Drone (Non - Educational Version I believe, but may still work with the educational version?)

Tested with Python 3.6, but it also may be compatabile with other versions.

## Example
Coming soon...

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
- 0: Set Drone distance to 0
- 1: Set Drone distance to 1
- 2: Set Drone distance to 2
- 3: Set Drone distance to 3
- 4: Set Drone distance to 4
- 5: Set Drone distance to 5
- 6: Set Drone distance to 6

#####Override Mode
- Backspace: Enable / Disable Override mode
- W/S: Fly Forward/Back
- A/D: Pan Left/Right
- Q/E: Fly Up/Down

## Roadmap
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
