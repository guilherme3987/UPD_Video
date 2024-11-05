import socket
import cv2
import pickle
import struct
import time
import pygame
from moviepy.editor import VideoFileClip
import numpy as np

# Endereço do servidor
server_ip = '127.0.0.1'
server_port = 12345

# Criando o socket do cliente
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip, server_port))

# Caminho do arquivo de vídeo
video_path = 'music.mp4'  # Caminho do arquivo de vídeo
# Abrindo o vídeo
cap = cv2.VideoCapture(video_path)

# Verificar se o vídeo foi aberto corretamente
if not cap.isOpened():
    print("Erro ao abrir o vídeo.")
    client_socket.close()
    exit()

# Reduzindo a resolução para 476x360 e ajustando a taxa de quadros
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 476)  # Largura do quadro
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)  # Altura do quadro
cap.set(cv2.CAP_PROP_FPS, 29.97)  # Taxa de quadros original

# Carregar o áudio com moviepy
video = VideoFileClip(video_path)
audio = video.audio
audio_fps = audio.fps  # Taxa de amostragem de áudio

# Inicializando o pygame para reproduzir áudio
pygame.mixer.init(frequency=int(audio_fps))

# Carregar o áudio para o pygame
audio_path = 'audio.wav'  # Vamos salvar o áudio em formato wav temporariamente
audio.write_audiofile(audio_path)

# Carregar o arquivo de áudio no pygame
sound = pygame.mixer.Sound(audio_path)

# Taxa de quadros do vídeo
fps = cap.get(cv2.CAP_PROP_FPS)
frame_interval = 1 / fps  # Intervalo entre os quadros

# Função para enviar o vídeo e o áudio
def send_video_audio():
    sound.play()  # Iniciar a reprodução do áudio

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Fim do vídeo.")
            break

        # Serializa o frame para envio
        frame_data = pickle.dumps(frame)
        message = struct.pack("Q", len(frame_data)) + frame_data  # Tamanho do frame + o próprio frame

        # Enviar pacote de vídeo
        client_socket.sendall(message)

        # Exibe o frame no cliente (opcional)
        #cv2.imshow("Enviando Video e Áudio", frame)

        # Aguarda para manter a taxa de quadros
        time.sleep(frame_interval)

        # Aguarda a tecla 'q' para parar
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    client_socket.close()
    cv2.destroyAllWindows()

# Iniciar envio de vídeo e áudio
send_video_audio()


#video_path = 'C:/Users/guilh/OneDrive/Área de Trabalho/Redes/UPD_Video/music.mp4'  # Caminho do arquivo de vídeo
