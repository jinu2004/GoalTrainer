import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

mp_drawing = mp.solutions.drawing_utils
base_options = python.BaseOptions(model_asset_path="resources/model.tflite")
options = vision.ObjectDetectorOptions(base_options=base_options, score_threshold=0.3)
detector = vision.ObjectDetector.create_from_options(options)


cap = cv2.VideoCapture("resources/WhatsApp Video 2023-10-30 at 4.41.47 PM.mp4")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
    results = detector.detect(mp_image)
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

            w = origin_x - origin_x + width

            real_ballWidth = 30
            real_distance_of_wall_from_camera = 50
            f = (w * real_distance_of_wall_from_camera) / real_ballWidth
            print(f)

            # Finding distance
            f = 840
            d = (real_ballWidth * f) / w
            print(d)

    cv2.imshow("Custom Object Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
