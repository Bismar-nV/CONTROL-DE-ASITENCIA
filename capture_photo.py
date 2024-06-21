import cv2
import os
import imutils
import sys

def capture_photo(person_name):
    data_path = r'E:\proyectos finales\proyecto final PDI 2024\flet-main\Form_CRUD\fotos'
    person_path = os.path.join(data_path, person_name)

    if not os.path.exists(person_path):
        print('Carpeta creada:', person_path)
        os.makedirs(person_path)

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Use the camera

    face_classif = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        frame = imutils.resize(frame, width=640)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        aux_frame = frame.copy()

        faces = face_classif.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            rostro = aux_frame[y:y + h, x:x + w]
            rostro = cv2.resize(rostro, (150, 150), interpolation=cv2.INTER_CUBIC)
            cv2.imwrite(os.path.join(person_path, 'rostro_{}.jpg'.format(count)), rostro)
            count += 1

        cv2.imshow('frame', frame)

        k = cv2.waitKey(1)
        if k == 27 or count >= 1:  # Captura una sola imagen
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    person_name = sys.argv[1]  # El nombre de la persona se pasa como argumento
    capture_photo(person_name)
