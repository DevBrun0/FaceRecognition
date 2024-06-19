import cv2
from cvzone.FaceDetectionModule import FaceDetector
import face_recognition
import os

#*Popup funtion is here*

detector = FaceDetector()
video = cv2.VideoCapture(0)

anchor_folder = 'data/anchor/'
anchor_encodings = []
anchor_names = []

# Load encodings and names from images in the anchor folder
for filename in os.listdir(anchor_folder):
    img_path = os.path.join(anchor_folder, filename)
    if os.path.isfile(img_path):
        if any(filename.lower().endswith(ext) for ext in ('.jpg', '.jpeg', '.png')):
            anchor_image = face_recognition.load_image_file(img_path)
            anchor_encoding = face_recognition.face_encodings(anchor_image)[0]
            anchor_encodings.append(anchor_encoding)
            anchor_names.append(os.path.splitext(filename)[0])

while True:
    ret, img = video.read()
    img, faces = detector.findFaces(img)

    # Verify if have or not face in camera
    if faces:
        # Catch the index of id(faces) of the camera
        for face in faces:
            # If don't exist face in camera the loop return
            if face['id'] != 0:
                pass
            else:
                # Covert the face in a trbl(top, right, bottom and left) format
                bbox = face['bbox']
                top, right, bottom, left = bbox[1], bbox[0] + bbox[2], bbox[1] + bbox[3], bbox[0]

                # Extract face encoding for the current face
                face_encoding = face_recognition.face_encodings(img, [(top, right, bottom, left)])[0]

                # Set defaut name as "Unknown"
                name = "Unknown"

                # Check for matches with anchor encodings
                for anchor_encoding in anchor_encodings:
                    # Compare face encoding with anchor encoding
                    match = face_recognition.compare_faces([anchor_encoding], face_encoding)[0]
                    if match:
                        name = "Known"
                        print(anchor_names)
                        break
                    #After compare the face in real time with database images 
                    #If this face is Unknown call the popup to register this face
                    #*Find a best practice to organize this code*

                # Draw bounding box and label on the face
                cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(img, name, (left, bottom - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    cv2.imshow("Result", img)

    if cv2.waitKey(1) == 27:  # Press 'Esc' key to exit
        break

video.release()
cv2.destroyAllWindows()
