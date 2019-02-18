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
Currently the controls often don't respond on the first press, you might have to spam the button. Will look into this bug in the future
- T: Takeoff
- L: To Land

## Roadmap
- Add a movement gradient dependent on distance from subject
- Add more to the facial recog to be able to tell when the drone needs to fly left or right
- Use pose estimation for input commands
- Add a function where the drone will ignore all faces except the one you specify
- Fix key pressing spam

# Credits
This script has been adapted from Damià Fuentes Escoté's [TelloSDKPy](https://github.com/damiafuentes/DJITelloPy) script, please check it out if you want to learn more about that.

#### AI
- **Jabrils**

#### Backend Thanks
- **Damià Fuentes Escoté** 
