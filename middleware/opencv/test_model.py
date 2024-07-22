import pickle

import cv2

from utils import get_face_landmarks


emotions = ['ANGER', 'HAPPINESS', 'NEUTRAL', 'SURPRISE']

with open('middleware/opencv/model', 'rb') as f:
    model = pickle.load(f)

cap = cv2.VideoCapture(0)

ret, frame = cap.read()


def resize_image(image, target_width, target_height):
    # Get current dimensions
    height, width = image.shape[:2]
    target_aspect_ratio = target_width / target_height
    current_aspect_ratio = width / height

    # Determine the cropping dimensions
    if current_aspect_ratio > target_aspect_ratio:
        # Crop the width
        new_width = int(height * target_aspect_ratio)
        offset = (width - new_width) // 2
        cropped_image = image[:, offset:offset + new_width]
    else:
        # Crop the height
        new_height = int(width / target_aspect_ratio)
        offset = (height - new_height) // 2
        cropped_image = image[offset:offset + new_height, :]

    # Resize the cropped image to the target dimensions
    resized_image = cv2.resize(cropped_image, (target_width, target_height))

    return resized_image


while ret:
    ret, frame = cap.read()

    frame = resize_image(frame, 200, 292)

    face_landmarks = get_face_landmarks(
        frame, draw=False, static_image_mode=False)

    if not face_landmarks:
        continue
    output = model.predict([face_landmarks])

    cv2.putText(frame,
                emotions[int(output[0])],
                (10, frame.shape[0] - 1),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                5)

    cv2.imshow('frame', frame)

    cv2.waitKey(25)


cap.release()
cv2.destroyAllWindows()
