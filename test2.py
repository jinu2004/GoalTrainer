import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import tensorflow as tf
import numpy as np
import time

mp_drawing = mp.solutions.drawing_utils
base_options = python.BaseOptions(model_asset_path="resources/model-fp16-gpu.tflite")
VisionRunningMode = mp.tasks.vision.RunningMode
options = vision.ObjectDetectorOptions(
    base_options=base_options,
    score_threshold=0.5,
    running_mode=VisionRunningMode.VIDEO,
)
detector = vision.ObjectDetector.create_from_options(options)


cap = cv2.VideoCapture("resources/WhatsApp Video 2023-10-30 at 4.41.47 PM.mp4")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.resize(frame,(640,640))
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
    timestamp_ms = int(time.time() * 1000)

    results = detector.detect_for_video(mp_image, timestamp_ms)
    # print(results)

    detections = results.detections
    if detections:  # Check if there are any detections
        for first_detection in detections:
            bounding_box = first_detection.bounding_box
            origin_x = bounding_box.origin_x
            origin_y = bounding_box.origin_y
            width = bounding_box.width
            height = bounding_box.height
            cv2.rectangle(
                frame,
                (origin_x, origin_y),
                (origin_x + width, origin_y + height),
                (0, 255, 0),
                2,
            )
            category = first_detection.categories[0]
            category_name = category.category_name
            score = category.score
            font = cv2.FONT_HERSHEY_SIMPLEX
            org = (50, 50)
            fontScale = 1
            color = (255, 0, 0)
            thickness = 2
            cv2.putText(
                frame,
                category_name + " " + str(score),
                (origin_x, origin_y),
                font,
                fontScale,
                color,
                thickness,
                cv2.LINE_AA,
            )

            orgins = [origin_x, origin_y]
            dimension = [width, height]
            print(orgins, dimension)

    cv2.imshow("Custom Object Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
