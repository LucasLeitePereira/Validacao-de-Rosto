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

nomeBusca = input("Seu nome: ")

sql = "SELECT rostos.shape, rostos.dtype, rostos.data FROM rostos INNER JOIN conta ON rostos.id_rosto = conta.id_rosto WHERE conta.nome_conta = %s"
cur.execute(sql, (nomeBusca,))

shape_s, dtype_s, blob = cur.fetchone()
shape = tuple(map(int, shape_s.split(",")))
img_result_encoding = np.frombuffer(blob, dtype=dtype_s).reshape(shape)

cap = cv2.VideoCapture(0)
ret, frame = cap.read()
cap.release()

if not ret:
    raise RuntimeError("Não conseguiu capturar o frame")

img_atual_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
img_atual_encoding = face_recognition.face_encodings(img_atual_rgb)[0]

result = face_recognition.compare_faces([img_atual_encoding], img_result_encoding)
if (result[0] == True):
    print("Acesso Liberado")
else:
    print("Acesso Negado")

fecharBancoDeDados(conn, cur)














