import socket
import time
import av
import struct

# Configurações do cliente
DEST_IP = '127.0.0.1'
DEST_PORT = 5004
#VIDEO_PATH = "C:/Users/guilh/OneDrive/Área de Trabalho/Redes/UPD_Video/meme.mp4"

VIDEO_PATH = "meme.mp4"


# Configurações RTP
SSRC = 12345  # Identificador da fonte, valor fixo neste exemplo
sequence_number = 0  # Número de sequência inicial
timestamp_increment = 3600  # Incremento de tempo entre quadros (ajuste conforme necessário)

def send_video(video_path):
    global sequence_number
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    container = av.open(video_path)
    timestamp = 0

    for frame in container.decode(video=0):
        payload = frame.to_ndarray().tobytes()
        timestamp += timestamp_increment

        # Fragmentação do payload e envio com cabeçalho RTP
        max_payload_size = 1400 - 12  # Subtraímos o tamanho do cabeçalho RTP
        for i in range(0, len(payload), max_payload_size):
            packet_payload = payload[i:i + max_payload_size]

            # Construção do cabeçalho RTP
            rtp_header = struct.pack('!BBHII',
                                     0x80,              # Versão 2
                                     96,                # Tipo de carga útil (não padrão para indicar dados de vídeo)
                                     sequence_number,   # Número de sequência
                                     timestamp,         # Timestamp
                                     SSRC)              # SSRC

            packet = rtp_header + packet_payload
            client_socket.sendto(packet, (DEST_IP, DEST_PORT))
            print(f"Enviando pacote de {len(packet)} bytes com sequência {sequence_number}")

            sequence_number += 1  # Incrementa o número de sequência

        time.sleep(0.04)  # Intervalo para 25 FPS

if __name__ == "__main__":
    send_video(VIDEO_PATH)
