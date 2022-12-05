from codecs import utf_8_decode
import socket
import threading
import requests
import json
import yaml
import base64

HEADER = 1000  #512 #Qt de caracteres permitidos em cada pacote
PORT = 5050

#SERVER = "127.0.0.1"
SERVER = socket.gethostbyname(socket.gethostname())

ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!SAIR"

ASPAS = "/*/*/aspas/*/*/"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr):
  print(f"[NOVA CONEXÃO] {addr} conectado.")

  # Capturar ativos do servidor

  connected = True
  while connected:
    msg = conn.recv(HEADER).decode()

    if str(msg) == DISCONNECT_MESSAGE:
      print(f"[DESCONECTANDO] {addr} desconectado.")
      connected = False
      break

    message = yaml.safe_load(msg)
    
    print(f"[{addr}] {message}")

  conn.close()


def start():
  server.listen()
  print(f"[ESCUTANDO] Servidor está escutando {SERVER}")
  while True:
    conn, addr = server.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()
    print(f"[CONEXÕES ATIVAS] {threading.activeCount() - 1}")


def send(msg, conn):
  conn.send(msg.encode())


print("[INICIANDO] Servidor está iniciando...")
start()
