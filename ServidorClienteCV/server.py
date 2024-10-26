import socket
import cv2
import numpy as np
import struct
import time

# Configurações do servidor
HOST = '127.0.0.1'
PORT = 5004

MAX_PACKET_SIZE = 1400
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
EXPECTED_FRAME_SIZE = FRAME_WIDTH * FRAME_HEIGHT * 3  # 3 bytes por pixel (RGB)

def start_server():
    # Configurações do socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((HOST, PORT))
    print(f"Servidor escutando em {HOST}:{PORT}")

    frame_data = b''  # Armazena bytes do frame atual
    expected_sequence = 0

    while True:
        # Recebe os dados do cliente
        data, addr = server_socket.recvfrom(MAX_PACKET_SIZE)

        # Lê o cabeçalho RTP (12 bytes)
        rtp_header = data[:12]
        payload = data[12:]

        # Desempacota o cabeçalho RTP
        _, _, sequence_number, timestamp, ssrc = struct.unpack('!BBHII', rtp_header)
        print(f"Recebido pacote de {len(payload)} bytes, sequência: {sequence_number}, timestamp: {timestamp}, SSRC: {ssrc}")

        # Verifica a sequência e adiciona o payload
        if sequence_number == expected_sequence:
            frame_data += payload
            expected_sequence += 1

            # Se o frame estiver completo, exibe-o
            if len(frame_data) >= EXPECTED_FRAME_SIZE:
                # Converte os bytes recebidos para um frame de imagem
                frame = np.frombuffer(frame_data[:EXPECTED_FRAME_SIZE], dtype=np.uint8).reshape((FRAME_HEIGHT, FRAME_WIDTH, 3))
                
                # Exibe o frame na janela OpenCV
                cv2.imshow('Servidor - Video Stream', frame)
                
                # Limpa os dados do frame para receber o próximo
                frame_data = frame_data[EXPECTED_FRAME_SIZE:]

                # Usa waitKey para manter a janela de vídeo ativa
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        else:
            print(f"Pacote fora de ordem: esperado {expected_sequence}, mas recebeu {sequence_number}")
            expected_sequence = sequence_number + 1  # Atualiza para manter a sincronia

        # Adiciona um atraso para observar as marcações de sequência e tempo
        time.sleep(0.1)

    # Fecha a janela OpenCV
    cv2.destroyAllWindows()

if __name__ == "__main__":
    start_server()
