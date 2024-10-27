import socket
import cv2
import numpy as np
import struct
import time

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
    expected_sequence = 0  # Controle do número de sequência esperado

    while True:
        # Recebe dados do cliente
        data, addr = server_socket.recvfrom(MAX_PACKET_SIZE)

        # Cabeçalho RTP (12 bytes)
        rtp_header = data[:12]
        payload = data[12:]

        # Desempacota o cabeçalho RTP
        version, payload_type, sequence_number, timestamp, ssrc = struct.unpack('!BBHII', rtp_header)
        print(f"Recebido pacote com sequência: {sequence_number}, timestamp: {timestamp}, SSRC: {ssrc}")

        # Verifica se o pacote está na sequência correta
        if sequence_number == expected_sequence:
            frame_data += payload
            expected_sequence += 1  # Atualiza o número de sequência esperado

            # Verifica se o frame foi completamente recebido
            if len(frame_data) >= FRAME_SIZE:
                print(f"Frame completo recebido com {len(frame_data)} bytes")

                try:
                    # Converte os dados do frame para uma imagem
                    frame = np.frombuffer(frame_data[:FRAME_SIZE], dtype=np.uint8).reshape((FRAME_HEIGHT, FRAME_WIDTH, 3))

                    # Exibe o frame usando OpenCV
                    cv2.imshow('Servidor - Video Stream', frame)

                except Exception as e:
                    print(f"Erro ao processar o frame: {e}")

                # Limpa o buffer para o próximo frame
                frame_data = frame_data[FRAME_SIZE:]

                # Atraso para simular uma taxa de quadros mais lenta e melhorar a visualização
                time.sleep(0.04)  # Aproximadamente 25 FPS

                # Fecha a janela quando a tecla 'q' for pressionada
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        else:
            # Caso o pacote esteja fora de ordem, descarta ou reordena conforme necessário
            print(f"Pacote fora de ordem: esperado {expected_sequence}, mas recebeu {sequence_number}")
            expected_sequence = sequence_number + 1  # Sincroniza para o próximo pacote

    # Fecha a janela OpenCV
    cv2.destroyAllWindows()

if __name__ == "__main__":
    start_server()
