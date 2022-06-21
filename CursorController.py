from imutils import face_utils
import numpy as np
import imutils
import dlib
import cv2
import logging as log
log.basicConfig(format='[%(levelname)s] %(message)s', level=log.DEBUG)
from Notifier import Notifier
from utils import get_resource_path

# Model
SHAPE_PREDICTOR = get_resource_path("model\landmark_predictor.dat")

# Threshold values and Frames
SHORT_BLINK_FRAMES = 3
LONG_BLINK_FRAMES = 7
EYEBROW_LIFT_FRAMES = 5
LONG_EYEBROW_LIFT_FRAMES = 10
EYEBROW_THRESH = 0.45
EYE_AR_LIFT_THRESH = 0.32
EYE_AR_THRESH = 0.19

# And some Constants
WHITE_COLOR = (255, 255, 255)
YELLOW_COLOR = (0, 255, 255)
RED_COLOR = (0, 0, 255)
GREEN_COLOR = (0, 255, 0)
BLUE_COLOR = (255, 0, 0)
BLACK_COLOR = (0, 0, 0)
TEAL_COLOR = (0, 220, 220)

# Grab the landmark indexes (custom model indexes)
lbStart, lbEnd = 0, 5
rbStart, rbEnd = 5, 10
nIndex = 10
lStart, lEnd = 11, 17
rStart, rEnd = 17, 23


resolution_w = 1366
resolution_h = 768
cam_w = 1080
cam_h = 720
unit_w = resolution_w / cam_w
unit_h = resolution_h / cam_h

class CursorController(Notifier):
    """ @param sensitivity: int - Mouse controls instance """

    def __init__(self, mouse_control):
        self._observers = []

        # Initialize counters
        self.eyebrow_lift_ctr = 0
        self.eye_closed_ctr = 0
        self.frame_ctr = 0
        self.anchor_point = (0, 0)

        # Booleans
        self.leftClick = False
        self.scroll = False
        self.input_mode = False
        self.scroll_mode = False
        self.faceDetected = False

        # HOG and Linear SVM supported face detector
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(SHAPE_PREDICTOR)

        # Mouse Control object
        self.mouse_control = mouse_control

    def setEyebrowLiftCtr(self):
        self.updatePercentage(self.eyebrow_lift_ctr*10)

    def toggleInputMode(self):
        self.input_mode = not self.input_mode
        self.changeInputMode(self.input_mode)

    def toggleScrollMode(self, value:bool):
        self.scroll_mode = value
        self.changeScrollMode(self.scroll_mode)

    def setFrame(self, frame):
        frame = cv2.flip(imutils.resize(frame, width=cam_w, height=cam_h), 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the grayscale frame
        rects = self.detector(gray, 0)

        # If Face detected, set faceDetected as true
        if len(rects) > 0:
            rect = rects[0]
            self.faceDetected = True
        else:
            self.faceDetected = False
            return frame
        
        # increment the frame counter
        self.frame_ctr += 1

        # Determine the facial landmarks for the face region, then convert the facial landmark (x, y)-coordinates to a NumPy array
        shape = self.predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)

        # Extract the left and right eye coordinates
        coordinates = self.extract_coordinates(shape)
        leftEye, rightEye, leftBrow, rightBrow, nose = coordinates
        
        # use the coordinates to compute the eye aspect ratio for both eyes
        leftEAR = self.eye_aspect_ratio(leftEye)
        rightEAR = self.eye_aspect_ratio(rightEye)
        ear = (leftEAR + rightEAR) / 2.0

        nose_point = nose

        # Mark the Landmarks
        # self.mark_landmarks(coordinates, frame)

        # if Eye is opened 
        if ear > EYE_AR_LIFT_THRESH:
            eyebrow_lifted = self.eyebrow_lift_ratio(leftEye, leftBrow, rightEye, rightBrow)
            
            # If eye is open and the eyebrow was lifted 
            if eyebrow_lifted > EYEBROW_THRESH:
                self.eyebrow_lift_ctr += 1
                self.setEyebrowLiftCtr()
                if self.eyebrow_lift_ctr == EYEBROW_LIFT_FRAMES:
                    self.scroll = True
                if self.eyebrow_lift_ctr == LONG_EYEBROW_LIFT_FRAMES:
                    self.toggleInputMode()
                    self.anchor_point = nose_point
                    self.scroll = False
            else:
                self.eyebrow_lift_ctr = 0
                self.setEyebrowLiftCtr()
                if self.scroll:
                    if self.scroll_mode:
                        self.toggleScrollMode(False)
                    elif self.input_mode:
                        self.toggleScrollMode(True)
                self.scroll = False
                    
        else:
            self.eyebrow_lift_ctr = 0
            self.setEyebrowLiftCtr()
            if self.scroll:
                if self.scroll_mode:
                    self.toggleScrollMode(False)
                elif self.input_mode:
                    self.toggleScrollMode(True)
            self.scroll = False

        # If eye is closed
        if ear < EYE_AR_THRESH and self.input_mode:
            self.eye_closed_ctr += 1
            
            if self.eye_closed_ctr == SHORT_BLINK_FRAMES:
                self.leftClick = True
                
            if self.eye_closed_ctr == LONG_BLINK_FRAMES:
                self.leftClick = False
                self.mouse_control.click("right")
                # _Debug_
                log.info("Right Click")
                self.eye_closed_ctr = 0
        else:
            if self.leftClick:
                self.mouse_control.click("left")
                # _Debug_
                log.info("Left Click")
                self.leftClick = False
            self.eye_closed_ctr = 0

        if self.input_mode:

            x, y = self.anchor_point
            w, h = 40, 25

            # Draw box around nose
            cv2.rectangle(frame, (x - w, y - h), (x + w, y + h), RED_COLOR, 5)
            cv2.line(frame, self.anchor_point, nose_point, RED_COLOR, 5)

            _direction, boost = self.direction(nose_point, self.anchor_point, w, h)

            if self.scroll_mode:
                self.mouse_control.scrollVertically(_direction, boost)
            else:
                self.mouse_control.moveMouse(_direction, boost)

        else:
            self.toggleScrollMode(False)
            
        if self.scroll_mode:
            pass

        return frame

    # utility functions
    def extract_coordinates(self, shape):
        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]
        leftBrow = shape[lbStart:lbEnd]
        rightBrow = shape[rbStart:rbEnd]
        nose = shape[nIndex]

        # Because I flipped the frame, left is right, right is left.
        leftEye, rightEye = rightEye, leftEye
        leftBrow, rightBrow = rightBrow, leftBrow

        return leftEye, rightEye, leftBrow, rightBrow, nose

    # def mark_landmarks(self, coordinates, frame):
        # Compute the convex hull for the left and right eye, then
        # visualize each of the eyes
        # leftBrowHull = cv2.convexHull(coordinates[2])
        # rightBrowHull = cv2.convexHull(coordinates[3])
        # leftEyeHull = cv2.convexHull(coordinates[0])
        # rightEyeHull = cv2.convexHull(coordinates[1])
        # cv2.drawContours(frame, [leftBrowHull], -1, YELLOW_COLOR, 4)
        # cv2.drawContours(frame, [rightBrowHull], -1, YELLOW_COLOR, 4)
        # cv2.drawContours(frame, [leftEyeHull], -1, YELLOW_COLOR, 4)
        # cv2.drawContours(frame, [rightEyeHull], -1, YELLOW_COLOR, 4)

        # for (x, y) in np.concatenate((coordinates[2], coordinates[3], coordinates[0], coordinates[1]), axis=0):
        #     cv2.circle(frame, (x, y), 2, GREEN_COLOR, -1)

        # nose_point = (coordinates[4][3, 0], coordinates[4][3, 1])
        # cv2.circle(frame, nose_point, 5, RED_COLOR, -1)


    # Returns EAR given eye landmarks
    def eye_aspect_ratio(self, eye):
        # Compute the euclidean distances between the vertical eye landmarks
        A = np.linalg.norm(eye[1] - eye[5])
        B = np.linalg.norm(eye[2] - eye[4])

        # Compute the euclidean distance between the horizontal eye landmarks
        C = np.linalg.norm(eye[0] - eye[3])

        # Compute the eye aspect ratio
        ear = (A + B) / (2.0 * C)

        # Return the eye aspect ratio
        return ear

    def eyebrow_lift_ratio(self, leftEye, leftEyeBrow, rightEye, rightEyeBrow) -> int:

        # Compute the euclidean distances between the vertical landmarks between eyelid and eyebrow
        LeftPt1 = np.linalg.norm(leftEyeBrow[2] - leftEye[1])
        LeftPt2 = np.linalg.norm(leftEyeBrow[3] - leftEye[2])
        LeftPt3 = np.linalg.norm(leftEyeBrow[0] - leftEyeBrow[4])
        left = ((LeftPt1 + LeftPt2) / (2 * LeftPt3))
        
        RightPt1 = np.linalg.norm(rightEyeBrow[1] - rightEye[1])
        RightPt2 = np.linalg.norm(rightEyeBrow[2] - rightEye[2])
        RightPt3 = np.linalg.norm(rightEyeBrow[0] - rightEyeBrow[4])
        right = ((RightPt1 + RightPt2) / (2 * RightPt3))
        
        # Stabilize the values
        if left < right*0.75:
            right = left
        elif right < left*0.75:
            left = right
        eyebrow_ratio = (left + right) / 2
        
        # Return the eyebrow ratio
        return eyebrow_ratio

    # Return direction given the nose and anchor points.
    def direction(self, nose_point, anchor_point, w, h):
        nx, ny = nose_point
        x, y = anchor_point
        boost = 1
        direction = 'none'

        diffX = abs(x-nx)
        diffY = abs(y-ny)

        if diffX > diffY:
            boost = diffX // w
            if boost > 1:
                boost = diffX // (w*2)
        else:
            boost = diffY // h
            if boost > 1:
                boost = diffY // (h*2)

        if boost > 3:
            boost = 3

        diffx, diffy = 0,0

        if nx > x + w:
            direction = 'right'
            diffx = nx - (x + w)
        elif nx < x - w:
            direction = 'left'
            diffx = (x - w) - nx

        if ny > y + h:
            diffy = ny - (y+h)
            if diffy > diffx:
                direction = 'down'
        elif ny < y - h:
            diffy = (y+h) - ny
            if diffy > diffx:
                direction = 'up'

        
        return direction, boost

    def show_debug_texts(self, frame, message, coord, color):
        cv2.putText(frame, message, coord, cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
    
    def __del__(self):
        # Destroy 
        log.debug("__del__() called at CursorController.py")
        cv2.destroyAllWindows()