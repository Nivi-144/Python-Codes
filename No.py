
import cv2
import numpy as np
import os

# Load COCO class names
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

# Load YOLOv3 model
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")

# Get output layer names
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

# Folder containing images
image_folder = "images"

# Process 10 images
for image_name in os.listdir(image_folder)[:10]:

    image_path = os.path.join(image_folder, image_name)

    # Read image
    image = cv2.imread(image_path)

    if image is None:
        continue

    height, width, channels = image.shape

    # Create input blob
    blob = cv2.dnn.blobFromImage(
        image,
        1 / 255.0,
        (416, 416),
        swapRB=True,
        crop=False
    )

    # Perform detection
    net.setInput(blob)
    outputs = net.forward(output_layers)

    boxes = []
    confidences = []
    class_ids = []

    # Process detections
    for output in outputs:
        for detection in output:

            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > 0.5:

                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)

                w = int(detection[2] * width)
                h = int(detection[3] * height)

                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # Remove overlapping boxes
    indexes = cv2.dnn.NMSBoxes(
        boxes,
        confidences,
        0.5,
        0.4
    )

    # Draw bounding boxes
    if len(indexes) > 0:

        for i in indexes.flatten():

            x, y, w, h = boxes[i]

            label = classes[class_ids[i]]
            confidence = confidences[i]

            cv2.rectangle(
                image,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

            text = f"{label}: {confidence:.2f}"

            cv2.putText(
                image,
                text,
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

            print(
                f"{image_name} -> {label}: {confidence:.2f}"
            )

    # Display result
    cv2.imshow("YOLOv3 Object Detection", image)

    cv2.waitKey(0)

cv2.destroyAllWindows()
