import face_recognition
import cv2
import numpy as np
from db_utils import get_db_connection, close_db_connection

def get_face_encoding_from_db(user_name):
    """Retrieves a user's face encoding from the database."""
    client, collection = get_db_connection()
    if client is None or collection is None:
        print("Exiting program due to database connection error.")
        return None

    try:
        # Query MongoDB for the user document
        user_document = collection.find_one({"nome_conta": user_name})

        if user_document and "face_encoding" in user_document:
            # Convert list back to numpy array
            return np.array(user_document["face_encoding"])
        else:
            print(f"No face encoding found for user: {user_name}")
            return None
    except Exception as e:
        print(f"Database error during face encoding retrieval: {e}")
        return None
    finally:
        close_db_connection(client)

def capture_current_face_encoding():
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

def validate_face(db_encoding, current_encoding):
    """Compares two face encodings and returns True if they match, False otherwise."""
    if db_encoding is None or current_encoding is None:
        return False
    
    # Compare faces using face_recognition library
    results = face_recognition.compare_faces([db_encoding], current_encoding)
    return results[0]

def main():
    user_name = input("Enter your name for validation: ")

    db_face_encoding = get_face_encoding_from_db(user_name)
    if db_face_encoding is None:
        return

    try:
        current_face_encoding = capture_current_face_encoding()
        if validate_face(db_face_encoding, current_face_encoding):
            print("Access Granted")
        else:
            print("Access Denied")
    except (IOError, RuntimeError, ValueError) as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
