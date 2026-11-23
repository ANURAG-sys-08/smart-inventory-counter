
from ultralytics import YOLO
import cv2

# Load pretrained YOLO model
model = YOLO("yolo11n.pt")


def detect_objects(image, confidence=0.35):
    """
    Detect objects in an image.

    Returns:
        annotated_image: image with bounding boxes
        detections: list of detected objects
    """

    results = model.predict(
        source=image,
        conf=confidence,
        verbose=False
    )

    result = results[0]

    annotated_image = result.plot()

    detections = []

    if result.boxes is not None:
        for box in result.boxes:

            class_id = int(box.cls[0])
            confidence_score = float(box.conf[0])

            object_name = model.names[class_id]

            detections.append({
                "name": object_name,
                "confidence": round(confidence_score, 3)
            })

    return annotated_image, detections
