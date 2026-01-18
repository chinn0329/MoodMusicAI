import cv2
import os

def capture_face_image(filename="temp_face.jpg"):
    cam = cv2.VideoCapture(0)

    if not cam.isOpened():
        return None

    ret, frame = cam.read()
    cam.release()

    if ret:
        cv2.imwrite(filename, frame)
        return filename

    return None


def delete_face_image(filename="temp_face.jpg"):
    if os.path.exists(filename):
        os.remove(filename)
