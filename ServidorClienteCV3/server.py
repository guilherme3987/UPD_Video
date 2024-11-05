import socket
import cv2
import pickle
import struct
import pygame

# Endereço e porta do servidor
server_ip = '127.0.0.1'
server_port = 12345

# Criando o socket do servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, server_port))
server_socket.listen(1)

print("Aguardando conexão do cliente...")
client_socket, client_address = server_socket.accept()
print(f"Conexão estabelecida com {client_address}")

# Inicializando o pygame para reprodução de áudio
pygame.mixer.init()

# Função para reproduzir áudio e exibir o vídeo
def receive_video_audio():
    audio_playing = False  # Flag para saber se o áudio já começou a tocar

    while True:
        # Receber o tamanho do quadro de vídeo
        frame_size_data = client_socket.recv(8)
        if not frame_size_data:
            break
        frame_size = struct.unpack("Q", frame_size_data)[0]

        # Receber o quadro de vídeo
        frame_data = b""
        while len(frame_data) < frame_size:
            frame_data += client_socket.recv(frame_size - len(frame_data))

        # Desserializar o quadro de vídeo
        frame = pickle.loads(frame_data)

        # Exibir o quadro do vídeo
        cv2.imshow("Recebendo Video e Áudio", frame)

        # Receber o bloco de áudio
        audio_size_data = client_socket.recv(8)
        if not audio_size_data:
            break
        audio_size = struct.unpack("Q", audio_size_data)[0]

        audio_data = b""
        while len(audio_data) < audio_size:
            audio_data += client_socket.recv(audio_size - len(audio_data))

        # Desserializar o bloco de áudio
        audio_block = pickle.loads(audio_data)

        # Se o áudio ainda não começou a tocar, inicie a reprodução
        if not audio_playing:
            sound = pygame.mixer.Sound(audio_block)
            sound.play()
            audio_playing = True

        # Aguarda para manter a taxa de quadros
        cv2.waitKey(1)

        # Se o usuário pressionar 'q', sai do loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Fechar as conexões e liberar os recursos
    client_socket.close()
    server_socket.close()
    cv2.destroyAllWindows()

# Iniciar recebimento de vídeo e áudio
receive_video_audio()
