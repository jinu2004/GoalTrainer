from tkinter import S
import cv2
import numpy as np
from cvzone import HandTrackingModule as hand
import time
import mediapipe as mp


def getScreen(img, arrayOfcorners):
    pts1 = np.float32(arrayOfcorners)
    width = -(arrayOfcorners[0][0] - arrayOfcorners[1][0])
    height = -(arrayOfcorners[0][1] - arrayOfcorners[2][1])

    pts2 = np.float32([[0, 0], [width, 0], [width, height], [0, height]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    result = cv2.warpPerspective(img, matrix, (width, height))

    return result


def drawRectangle(imgs, arrayOfCorners, thickness):
    cv2.line(
        imgs,
        (arrayOfCorners[0][0][0], arrayOfCorners[0][0][1]),
        (arrayOfCorners[1][0][0], arrayOfCorners[1][0][1]),
        (0, 255, 0),
        thickness,
    )
    cv2.line(
        imgs,
        (arrayOfCorners[0][0][0], arrayOfCorners[0][0][1]),
        (arrayOfCorners[2][0][0], arrayOfCorners[2][0][1]),
        (0, 255, 0),
        thickness,
    )
    cv2.line(
        imgs,
        (arrayOfCorners[3][0][0], arrayOfCorners[3][0][1]),
        (arrayOfCorners[2][0][0], arrayOfCorners[2][0][1]),
        (0, 255, 0),
        thickness,
    )
    cv2.line(
        imgs,
        (arrayOfCorners[3][0][0], arrayOfCorners[3][0][1]),
        (arrayOfCorners[1][0][0], arrayOfCorners[1][0][1]),
        (0, 255, 0),
        thickness,
    )

    return imgs


class Calibrate:
    def __init__(self, width, height, camera_index, windowname):
        self.is_selecting = True
        self.corner_points = []
        self.width = width
        self.windowname = windowname
        self.height = height
        self.camera_index = camera_index
        self.mouseEventWindow = "Select corners clockwise order"
        self.cap = cv2.VideoCapture(self.camera_index)
        self.image = None
        self.is_enabled = False
        self.imageWarped = None

    def __mouse_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            if self.is_selecting:
                self.corner_points.append((x, y))
                if len(self.corner_points) == 4:
                    self.is_selecting = False

    def getScreen_for_track(self):
        self.imageWarped = getScreen(self.image, self.corner_points)
        # self.imageWarped = cv2.resize(self.imageWarped, (self.width, self.height))
        # cv2.imshow(self.windowname, self.imageWarped)
        return self.imageWarped

    def setup(self):
        cv2.namedWindow(self.mouseEventWindow)
        cv2.setMouseCallback(self.mouseEventWindow, self.__mouse_callback)

    def loop(self):
        self.is_enabled, self.image = self.cap.read()
        if self.is_enabled:
            for point in self.corner_points:
                cv2.circle(self.image, point, 5, (0, 0, 255), -1)
            cv2.imshow(self.mouseEventWindow, self.image)

            if not self.is_selecting:
                image = self.getScreen_for_track()
                # cv2.imshow(self.windowname, image)

        else:
            print("cannot open camera")
            return
