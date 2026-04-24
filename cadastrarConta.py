import face_recognition
import cv2
import numpy as np
import psycopg2
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
    """Registers user information and their face encoding in the database."""
    conn, cur = get_db_connection()
    if conn is None or cur is None:
        print("Exiting program due to database connection error.")
        return

    try:
        # Convert face encoding to a format suitable for PostgreSQL
        arr = np.array(face_encoding, dtype=np.float64)
        shape = ",".join(map(str, arr.shape))
        dtype = str(arr.dtype)
        blob = arr.tobytes()

        # Insert face encoding into 'rostos' table
        cur.execute(
            "INSERT INTO rostos (shape, dtype, data) VALUES (%s, %s, %s) RETURNING id_rosto",
            (shape, dtype, psycopg2.Binary(blob))
        )
        id_rosto = cur.fetchone()[0]

        # Insert user account details into 'conta' table
        sql = "INSERT INTO conta (nome_conta, idade, sexo, id_rosto) VALUES (%s, %s, %s, %s)"
        cur.execute(sql, (name, age, gender, id_rosto))
        conn.commit()
        print(f"User {name} registered successfully with face ID {id_rosto}.")

    except psycopg2.Error as e:
        conn.rollback()
        print(f"Database error during registration: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        close_db_connection(conn, cur)

def main():
    name = input("Enter your name: ")
    age = int(input("Enter your age: "))
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
