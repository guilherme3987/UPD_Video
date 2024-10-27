'''
Servidor que encapsula quadros de video armazenado dentro de pacotes RTP

Baixa resolução: 240p ou 360p, para que o tamanho de cada quadro de vídeo seja pequeno.
Baixa taxa de quadros (frame rate): 15 ou 24 FPS, o que reduz a quantidade de quadros processados por segundo.
Curta duração: 10 a 30 segundos, para que o teste não leve muito tempo.

'''
import socket
import cv2
import numpy as np

# Configurações do servidor
HOST = '127.0.0.1'  # Escuta no localhost
PORT = 5004         # Porta que o servidor escuta
MAX_PACKET_SIZE = 1400  # Tamanho máximo do pacote
FRAME_WIDTH = 640   # Largura do frame
FRAME_HEIGHT = 480  # Altura do frame
FRAME_SIZE = FRAME_WIDTH * FRAME_HEIGHT * 3  # Tamanho total do frame (RGB)

def start_server():
    # Cria um socket UDP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((HOST, PORT))
    print(f"Servidor escutando em {HOST}:{PORT}")

    frame_data = b''  # Armazena os bytes do frame atual

    while True:
        # Recebe dados do cliente
        data, addr = server_socket.recvfrom(MAX_PACKET_SIZE)
        print(f"Recebido {len(data)} bytes de {addr}")

        # Monta o frame com os pacotes recebidos
        frame_data += data

        # Verifica se o frame está completo
        if len(frame_data) >= FRAME_SIZE:
            # Converte os dados do frame para uma imagem
            frame = np.frombuffer(frame_data[:FRAME_SIZE], dtype=np.uint8).reshape((FRAME_HEIGHT, FRAME_WIDTH, 3))

            # Exibe o frame usando OpenCV
            cv2.imshow('Servidor - Video Stream', frame)

            # Limpa o buffer para o próximo frame
            frame_data = frame_data[FRAME_SIZE:]

            # Fecha a janela quando a tecla 'q' for pressionada
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # Fecha a janela OpenCV
    cv2.destroyAllWindows()

if __name__ == "__main__":
    start_server()

