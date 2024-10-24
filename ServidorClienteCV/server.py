import socket
import cv2
import numpy as np

HOST = '127.0.0.1'  
PORT = 5004 

# Tamanho máximo do pacote (igual ao cliente)
MAX_PACKET_SIZE = 1400

# Resolução do frame
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
EXPECTED_FRAME_SIZE = FRAME_WIDTH * FRAME_HEIGHT * 3  # 3 bytes por pixel (RGB)

def start_server():
    # Cria um socket UDP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((HOST, PORT))
    print(f"Servidor escutando em {HOST}:{PORT}")

    frame_data = b''  # Armazena os bytes do frame atual

    while True:
        # Recebe dados do cliente
        data, addr = server_socket.recvfrom(MAX_PACKET_SIZE)  # Tamanho máximo do datagrama
        print(f"Recebido {len(data)} bytes de {addr}")

        # Adiciona os dados recebidos ao frame atual
        frame_data += data

        # Verifica se o frame foi totalmente recebido
        while len(frame_data) >= EXPECTED_FRAME_SIZE:
            # Converte os bytes recebidos de volta para um frame de imagem
            frame = np.frombuffer(frame_data[:EXPECTED_FRAME_SIZE], dtype=np.uint8).reshape((FRAME_HEIGHT, FRAME_WIDTH, 3))

            # Exibe o frame
            cv2.imshow('Servidor - Video Stream', frame)

            # Limpa os dados para o próximo frame
            frame_data = frame_data[EXPECTED_FRAME_SIZE:]  # Remove os bytes já processados

            # Fecha a janela quando a tecla 'q' for pressionada
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # Fecha a janela OpenCV
    cv2.destroyAllWindows()

if __name__ == "__main__":
    start_server()