import face_recognition
import cv2
import psycopg2
import numpy as np

def abrirBancoDeDados():
    try:
        conn = psycopg2.connect(
            host="",
            port=,
            dbname="",
            user="",
            password=""
        )
        cur = conn.cursor()
        print("Banco de dados aberto")
        return conn, cur
    except psycopg2.Error as e:
        print(f"Não conseguiu abrir o banco de dados: {e}")
        return None, None

def fecharBancoDeDados(conn, cur):
    if cur:
        cur.close()
    if conn:
        conn.close()
    print("Banco de dados fechado")

conn, cur = abrirBancoDeDados()

if conn is None or cur is None:
    print("Encerrando o programa devido a erro no banco de dados.")
    exit(1)

nome = input("Seu nome:")
idade = int(input("Idade: "))
sexo = input("Sexo: ")

cap = cv2.VideoCapture(0)
ret, frame = cap.read()
cap.release()

if not ret:
    raise RuntimeError("Não conseguiu capturar o frame")
else:
    print("Imagem capturada com sucesso")

# Codifica o frame como JPEG
rgb_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
img_encoding = face_recognition.face_encodings(rgb_img)[0]

arr = np.array(img_encoding, dtype=np.float64)

shape = ",".join(map(str, arr.shape))   # e.g. "128,"
dtype = str(arr.dtype)                  # e.g. "float64"
blob  = arr.tobytes()                   # raw bytes

cur.execute(
  "INSERT INTO rostos (shape, dtype, data) VALUES (%s,%s,%s)",
  (shape, dtype, psycopg2.Binary(blob))
)

conn.commit()

cur.execute("select max(id_rosto) from rostos")
id_rosto = cur.fetchone()[0]

sql = "INSERT INTO conta (nome_conta, idade, sexo, id_rosto) VALUES (%s, %s, %s, %s)"
cur.execute(sql, (nome, idade, sexo, id_rosto))
conn.commit()


fecharBancoDeDados(conn, cur)