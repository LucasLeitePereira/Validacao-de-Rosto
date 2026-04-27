import face_recognition
import cv2
import numpy as np
import base64
from db_utils import get_db_connection, close_db_connection

def capture_face_encoding():
    """Captures a face from the webcam and returns its encoding."""
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise IOError("Cannot open webcam")

    ret, frame = cap.read()
    cap.release()

    if not ret:
        raise RuntimeError("Failed to capture frame from webcam.")
    
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_encodings = face_recognition.face_encodings(rgb_frame)
    
    if not face_encodings:
        raise ValueError("No face detected in the captured image.")
        
    return face_encodings[0]

def register_user_and_face(name, age, gender, face_encoding):
    """Registers user information and their face encoding in MongoDB."""
    client, collection = get_db_connection()
    if client is None or collection is None:
        print("Exiting program due to database connection error.")
        return

    try:
        # Convert face encoding to a format suitable for MongoDB
        # We store the encoding as a list of floats or a base64 encoded string
        # For simplicity and readability in NoSQL, a list of floats is common
        face_encoding_list = face_encoding.tolist()

        user_document = {
            "name": name,
            "age": age,
            "gender": gender,
            "face_encoding": face_encoding_list
        }

        result = collection.insert_one(user_document)
        print(f"User {name} registered successfully with ID {result.inserted_id}.")

    except Exception as e:
        print(f"An error occurred during registration: {e}")
    finally:
        close_db_connection(client)

def main():
    name = input("Enter your name: ")
    try:
        age = int(input("Enter your age: "))
    except ValueError:
        print("Invalid age. Please enter a number.")
        return
    gender = input("Enter your gender: ")

    try:
        face_encoding = capture_face_encoding()
        register_user_and_face(name, age, gender, face_encoding)
    except (IOError, RuntimeError, ValueError) as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
