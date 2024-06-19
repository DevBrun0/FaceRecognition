import cv2
from cvzone.FaceDetectionModule import FaceDetector
import face_recognition
import os

detector = FaceDetector()
video = cv2.VideoCapture(0)

anchor_folder = 'data/anchor/'
anchor_encodings = []
anchor_names = []

while True:
    ret, img = video.read()
    img, faces = detector.findFaces(img)

    if faces:
        for face in faces:
            if face['id'] != 0:
                pass
            else:
                # Convert the face bounding box to (top, right, bottom, left) format
                bbox = face['bbox']
                top, right, bottom, left = bbox[1], bbox[0] + bbox[2], bbox[1] + bbox[3], bbox[0]

                # Extract face encoding for the current face
                face_encoding = face_recognition.face_encodings(img, [(top, right, bottom, left)])[0]

                # Set default name as "Unknown"
                name = "Unknown"

                # Check for matches with anchor encodings
                for anchor_encoding in anchor_encodings:
                    # Compare face encoding with anchor encoding
                    match = face_recognition.compare_faces([anchor_encoding], face_encoding)[0]
                    if match:
                        name = "Known"
                        print(anchor_names)
                        break

                # Draw bounding box and label on the face
                cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(img, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    cv2.imshow("Result", img)

    if cv2.waitKey(1) == 27:  # Press 'Esc' key to exit
        break

video.release()
cv2.destroyAllWindows()
