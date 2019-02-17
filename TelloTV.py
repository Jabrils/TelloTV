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
tDistance = args.distance

# Frames per second of the pygame window display
FPS = 25
dimensions = (960, 720)


# 
face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()

if args.save_session:
    ddir = "Sessions"
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

            if args.save_session:
                cv2.imwrite("{}/tellocap{}.jpg".format(ddir,imgCount),frame_read.frame)
            
            frame = np.rot90(frame)
            imgCount+=1

            time.sleep(1 / FPS)

            # Press T to take off
            if cv2.waitKey(20) & 0xFF == ord('t'):
                if not args.debug:
                    print("Taking Off")
                    self.tello.takeoff()
                    self.tello.get_battery()
                self.send_rc_control = True

            # Press L to land
            if cv2.waitKey(20) & 0xFF == ord('l'):
                if not args.debug:
                    print("Landing")
                    self.tello.land()
                self.send_rc_control = False

            gray  = cv2.cvtColor(frameRet, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=2)

            # Target size
            tSize = faceSizes[tDistance]

            # Gets the width & height of the frame
            width = 960
            height = 720

            # These are our center dimensions
            cWidth = int(width/2)
            cHeight = int(height/2)

            noFaces = len(faces) == 0

            # if we've given rc controls & get face coords returned
            if self.send_rc_control:
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

                        # for forward back
                        if vDistance[2] > 0:
                            self.for_back_velocity = S
                        elif vDistance[2] < 0:
                            self.for_back_velocity = -S
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

            # Draw the distance choosen
            cv2.putText(frameRet,str(tDistance),(32,664),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)


            # Display the resulting frame
            cv2.imshow(f'Tello Tracking...',frameRet)

            # Quit the software
            if cv2.waitKey(20) & 0xFF == ord('q'):
                should_stop = True
                break

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


def main():
    frontend = FrontEnd()

    # run frontend
    frontend.run()


if __name__ == '__main__':
    main()
