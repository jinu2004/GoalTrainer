import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import time


class Object:
    def __init__(self, model_path, score_threshold=0.5):
        self.model_path = model_path
        self.score_threshold = score_threshold
        self.VisionRunningMode = mp.tasks.vision.RunningMode
        self.base_options = python.BaseOptions(model_asset_path=model_path)
        self.options = vision.ObjectDetectorOptions(
            base_options=self.base_options,
            score_threshold=self.score_threshold,
            running_mode=self.VisionRunningMode.VIDEO,
            max_results=1,
        )
        self.detector = vision.ObjectDetector.create_from_options(self.options)

    def Track_Objecte(self, frame):
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        timestamp_ms = int(time.time() * 1000)

        results = self.detector.detect_for_video(mp_image, timestamp_ms)
        x = 0
        y = 0
        width = 0
        height = 0
        # print(results)
        detections = results.detections
        if detections:  # Check if there are any detections
            for first_detection in detections:
                bounding_box = first_detection.bounding_box
                origin_x = bounding_box.origin_x
                origin_y = bounding_box.origin_y
                width_B = bounding_box.width
                height_B = bounding_box.height
                cv2.rectangle(
                    frame,
                    (origin_x, origin_y),
                    (origin_x + width_B, origin_y + height_B),
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
                x = origin_x
                y = origin_y
                width = width_B
                height = height_B

        return x, y, width, height, frame
