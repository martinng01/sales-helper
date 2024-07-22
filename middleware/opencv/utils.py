import cv2
import mediapipe as mp


def get_face_landmarks(image: cv2.typing.MatLike, draw=False, static_image_mode=True):

    # Read the input image
    image_input_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    face_mesh = mp.solutions.face_mesh.FaceMesh(
        static_image_mode=static_image_mode,
        max_num_faces=1,
        min_detection_confidence=0.5
    )
    image_rows, image_cols, _ = image.shape
    results = face_mesh.process(image_input_rgb)

    image_landmarks = []

    if results.multi_face_landmarks:

        if draw:

            mp_drawing = mp.solutions.drawing_utils
            mp_drawing_styles = mp.solutions.drawing_styles
            drawing_spec = mp_drawing.DrawingSpec(thickness=2, circle_radius=1)

            mp_drawing.draw_landmarks(
                image=image,
                landmark_list=results.multi_face_landmarks[0],
                connections=mp.solutions.face_mesh.FACEMESH_CONTOURS,
                landmark_drawing_spec=drawing_spec,
                connection_drawing_spec=drawing_spec)

        ls_single_face = results.multi_face_landmarks[0].landmark
        xs_ = []
        ys_ = []
        zs_ = []
        for idx in ls_single_face:
            xs_.append(idx.x)
            ys_.append(idx.y)
            zs_.append(idx.z)
        for j in range(len(xs_)):
            image_landmarks.append(xs_[j] - min(xs_))
            image_landmarks.append(ys_[j] - min(ys_))
            image_landmarks.append(zs_[j] - min(zs_))

    return image_landmarks


def resize_image(image: cv2.typing.MatLike, target_width: int, target_height: int) -> cv2.typing.MatLike:
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
    resized_image = cv2.resize(
        cropped_image, (target_width, target_height))

    return resized_image
