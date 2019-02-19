from djitellopy import Tello
import cv2
import numpy as np
import time
import datetime
import os
import argparse

# standard argparse stuff
parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, add_help=False)
parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,
                    help='** = required')
parser.add_argument('-d', '--distance', type=int, default=3,
    help='use -d to change the distance of the drone. Range 0-6')
parser.add_argument('-ss', "--save_session", action='store_true',
    help='add the -ss flag to save your session as an image sequence in the Sessions folder')
parser.add_argument('-D', "--debug", action='store_true',
    help='add the -D flag to enable debug mode. Everything works the same, but no commands will be sent to the drone')

args = parser.parse_args()

# Speed of the drone
S = 20
S2 = 5
UDOffset = 150

# this is just the bound box sizes that openCV spits out *shrug*
faceSizes = [1026, 684, 456, 304, 202, 136, 90]

# These are the values in which kicks in speed up mode, as of now, this hasn't been finalized or fine tuned so be careful
# Tested are 3, 4, 5
acc = [500,250,250,150,110,70,50]

# Frames per second of the pygame window display
FPS = 25
dimensions = (960, 720)

# 
face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()

# If we are to save our sessions, we need to make sure the proper directories exist
if args.save_session:
    ddir = "Sessions"

    if not os.path.isdir(ddir):
        os.mkdir(ddir)

    ddir = "Sessions/Session {}".format(str(datetime.datetime.now()).replace(':','-').replace('.','_'))
    os.mkdir(ddir)

class FrontEnd(object):
    
    def __init__(self):
        # Init Tello object that interacts with the Tello drone
        self.tello = Tello()

        # Drone velocities between -100~100
        self.for_back_velocity = 0
        self.left_right_velocity = 0
        self.up_down_velocity = 0
        self.yaw_velocity = 0
        self.speed = 10

        self.send_rc_control = False

    def run(self):

        if not self.tello.connect():
            print("Tello not connected")
            return

        if not self.tello.set_speed(self.speed):
            print("Not set speed to lowest possible")
            return

        # In case streaming is on. This happens when we quit this program without the escape key.
        if not self.tello.streamoff():
            print("Could not stop video stream")
            return

        if not self.tello.streamon():
            print("Could not start video stream")
            return

        frame_read = self.tello.get_frame_read()

        should_stop = False
        imgCount = 0
        OVERRIDE = False
        tDistance = args.distance
        self.tello.get_battery()

        if args.debug:
            print("DEBUG MODE ENABLED!")

        while not should_stop:
            self.update()

            if frame_read.stopped:
                frame_read.stop()
                break

            theTime = str(datetime.datetime.now()).replace(':','-').replace('.','_')

            frame = cv2.cvtColor(frame_read.frame, cv2.COLOR_BGR2RGB)
            frameRet = frame_read.frame

            vid = self.tello.get_video_capture()

            if args.save_session:
                cv2.imwrite("{}/tellocap{}.jpg".format(ddir,imgCount),frameRet)
            
            frame = np.rot90(frame)
            imgCount+=1

            time.sleep(1 / FPS)

            # 
            k = cv2.waitKey(20)

            # Press 0 to set distance to 0
            if k == ord('0'):
                print("Distance = 0")
                tDistance = 0

            # Press 1 to set distance to 1
            if k == ord('1'):
                print("Distance = 1")
                tDistance = 1

            # Press 2 to set distance to 2
            if k == ord('2'):
                print("Distance = 2")
                tDistance = 2
                    
            # Press 3 to set distance to 3
            if k == ord('3'):
                print("Distance = 3")
                tDistance = 3
            
            # Press 4 to set distance to 4
            if k == ord('4'):
                print("Distance = 4")
                tDistance = 4
                    
            # Press 5 to set distance to 5
            if k == ord('5'):
                print("Distance = 5")
                tDistance = 5
                    
            # Press 6 to set distance to 6
            if k == ord('6'):
                print("Distance = 6")
                tDistance = 6

            # Press T to take off
            if k == ord('t'):
                if not args.debug:
                    print("Taking Off")
                    self.tello.takeoff()
                    self.tello.get_battery()
                self.send_rc_control = True

            # Press L to land
            if k == ord('l'):
                if not args.debug:
                    print("Landing")
                    self.tello.land()
                self.send_rc_control = False

            # Press Backspace for controls override
            if k == 8:
                if not OVERRIDE:
                    OVERRIDE = True
                    print("OVERRIDE ENABLED")
                else:
                    OVERRIDE = False
                    print("OVERRIDE DISABLED")

            if OVERRIDE:
                # Press 6 to set distance to 6
                if k == ord('w'):
                    self.for_back_velocity = int(S * 2)
                elif k == ord('s'):
                    self.for_back_velocity = -int(S * 2)
                else:
                    self.for_back_velocity = 0

                # Press 6 to set distance to 6
                if k == ord('a'):
                    self.yaw_velocity = int(S * 2)
                elif k == ord('d'):
                    self.yaw_velocity = -int(S * 2)
                else:
                    self.yaw_velocity = 0

                # Press 6 to set distance to 6
                if k == ord('q'):
                    self.up_down_velocity = int(S * 2)
                elif k == ord('e'):
                    self.up_down_velocity = -int(S * 2)
                else:
                    self.up_down_velocity = 0


            # Quit the software
            if k == 27:
                should_stop = True
                break

            gray  = cv2.cvtColor(frameRet, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=2)

            # Target size
            tSize = faceSizes[tDistance]

            # These are our center dimensions
            cWidth = int(dimensions[0]/2)
            cHeight = int(dimensions[1]/2)

            noFaces = len(faces) == 0

            # if we've given rc controls & get face coords returned
            if self.send_rc_control and not OVERRIDE:
                for (x, y, w, h) in faces:

                    # 
                    roi_gray = gray[y:y+h, x:x+w] #(ycord_start, ycord_end)
                    roi_color = frameRet[y:y+h, x:x+w]

                    # setting Face Box properties
                    fbCol = (255, 0, 0) #BGR 0-255 
                    fbStroke = 2
                    
                    # end coords are the end of the bounding box x & y
                    end_cord_x = x + w
                    end_cord_y = y + h
                    end_size = w*2

                    # these are our target coordinates
                    targ_cord_x = int((end_cord_x + x)/2)
                    targ_cord_y = int((end_cord_y + y)/2) + UDOffset

                    # This calculates the vector from your face to the center of the screen
                    vTrue = np.array((cWidth,cHeight,tSize))
                    vTarget = np.array((targ_cord_x,targ_cord_y,end_size))
                    vDistance = vTrue-vTarget

                    # Safety Zone X
                    szX = 100

                    # Safety Zone Y
                    szY = 55

                    # 
                    if not args.debug:
                        # for turning
                        if vDistance[0] < -szX:
                            self.yaw_velocity = S
                            # self.left_right_velocity = S2
                        elif vDistance[0] > szX:
                            self.yaw_velocity = -S
                            # self.left_right_velocity = -S2
                        else:
                            self.yaw_velocity = 0
                        
                        # for up & down
                        if vDistance[1] > szY:
                            self.up_down_velocity = S
                        elif vDistance[1] < -szY:
                            self.up_down_velocity = -S
                        else:
                            self.up_down_velocity = 0

                        F = 0
                        if abs(vDistance[2]) > acc[tDistance]:
                            F = S

                        # for forward back
                        if vDistance[2] > 0:
                            self.for_back_velocity = S + F
                        elif vDistance[2] < 0:
                            self.for_back_velocity = -S - F
                        else:
                            self.for_back_velocity = 0

                    # Draw the face bounding box
                    cv2.rectangle(frameRet, (x, y), (end_cord_x, end_cord_y), fbCol, fbStroke)

                    # Draw the target as a circle
                    cv2.circle(frameRet, (targ_cord_x, targ_cord_y), 10, (0,255,0), 2)

                    # Draw the safety zone
                    cv2.rectangle(frameRet, (targ_cord_x - szX, targ_cord_y - szY), (targ_cord_x + szX, targ_cord_y + szY), (0,255,0), fbStroke)

                    # Draw the estimated drone vector position in relation to face bounding box
                    cv2.putText(frameRet,str(vDistance),(0,64),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)

                # if there are no faces detected, don't do anything
                if noFaces:
                    self.yaw_velocity = 0
                    self.up_down_velocity = 0
                    self.for_back_velocity = 0
                    print("NO TARGET")
                
            # Draw the center of screen circle, this is what the drone tries to match with the target coords
            cv2.circle(frameRet, (cWidth, cHeight), 10, (0,0,255), 2)

            dCol = lerp(np.array((0,0,255)),np.array((255,255,255)),tDistance+1/7)

            if OVERRIDE:
                show = "OVERRIDE"
            else:
                show = str(tDistance)

            # Draw the distance choosen
            cv2.putText(frameRet,show,(32,664),cv2.FONT_HERSHEY_SIMPLEX,1,dCol,2)

            # Display the resulting frame
            cv2.imshow(f'Tello Tracking...',frameRet)

        # On exit, print the battery
        self.tello.get_battery()

        # When everything done, release the capture
        cv2.destroyAllWindows()
        
        # Call it always before finishing. I deallocate resources.
        self.tello.end()


    def battery(self):
        return self.tello.get_battery()[:2]

    def update(self):
        """ Update routine. Send velocities to Tello."""
        if self.send_rc_control:
            self.tello.send_rc_control(self.left_right_velocity, self.for_back_velocity, self.up_down_velocity,
                                       self.yaw_velocity)

def lerp(a,b,c):
    return a + c*(b-a)

def main():
    frontend = FrontEnd()

    # run frontend
    frontend.run()


if __name__ == '__main__':
    main()
