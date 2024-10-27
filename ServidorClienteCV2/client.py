import socket
import time
import av
import struct

# Configurações do cliente
DEST_IP = '127.0.0.1'  # IP do servidor (localhost para teste)
DEST_PORT = 5004       # Porta do servidor
#VIDEO_PATH = "meme.mp4"  # Caminho do vídeo a ser enviado
VIDEO_PATH = "C:/Users/guilh/OneDrive/Área de Trabalho/Redes/UPD_Video/meme.mp4"  # Caminho do vídeo a ser enviado

SSRC = 12345  # Identificador da fonte
sequence_number = 0  # Número de sequência inicial
timestamp_increment = 3600  # Incremento do timestamp (ajustar conforme necessário)

# Função para enviar vídeo usando RTP
def send_video(video_path):
    global sequence_number
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Abre o vídeo usando PyAV
    container = av.open(video_path)
    timestamp = 0

    for frame in container.decode(video=0):
        # Converte o quadro para bytes
        payload = frame.to_rgb().to_ndarray().tobytes()
        timestamp += timestamp_increment

        # Fragmenta o payload e adiciona o cabeçalho RTP
        max_payload_size = 1400 - 12  # Subtraímos 12 bytes para o cabeçalho RTP
        for i in range(0, len(payload), max_payload_size):
            packet_payload = payload[i:i + max_payload_size]

            # Construção do cabeçalho RTP
            rtp_header = struct.pack('!BBHII',
                                     0x80,              # Versão RTP (2 bits)
                                     96,                # Tipo de carga útil (96 para vídeo não padrão)
                                     sequence_number,   # Número de sequência
                                     timestamp,         # Timestamp
                                     SSRC)              # SSRC (identificador da fonte)

            # Montagem do pacote RTP (cabeçalho + payload)
            packet = rtp_header + packet_payload
            client_socket.sendto(packet, (DEST_IP, DEST_PORT))
            print(f"Enviando pacote de {len(packet)} bytes com sequência {sequence_number}")

            # Incrementa o número de sequência
            sequence_number += 1

        # Aguarda um pequeno intervalo para simular a taxa de quadros do vídeo (25 FPS)
        time.sleep(0.04)

if __name__ == "__main__":
    send_video(VIDEO_PATH)
