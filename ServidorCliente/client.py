import socket
import time
import av

# Configurações do cliente
DEST_IP = '127.0.0.1'  # IP do servidor (localhost para teste)
DEST_PORT = 5004        # Porta do servidor
VIDEO_PATH = "C:/Users/guilh/OneDrive/Área de Trabalho/Redes/UPD_Video/meme.mp4" # Caminho do vídeo a ser enviado

# Função para enviar dados para o servidor
def send_video(video_path):
    # Cria um socket UDP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Abre o vídeo usando PyAV
    container = av.open(video_path)

    for frame in container.decode(video=0):
        # Converte o quadro para bytes
        payload = frame.to_ndarray().tobytes()
        
        # Fragmenta o payload se necessário
        max_packet_size = 1400  # Tamanho máximo para o pacote
        for i in range(0, len(payload), max_packet_size):
            packet = payload[i:i + max_packet_size]
            client_socket.sendto(packet, (DEST_IP, DEST_PORT))
            print(f"Enviando quadro de {len(packet)} bytes para {DEST_IP}:{DEST_PORT}")

        # Aguarda um pequeno intervalo para simular a taxa de quadros do vídeo
        time.sleep(0.04)  # Por exemplo, 25 FPS


if __name__ == "__main__":
    send_video(VIDEO_PATH)
