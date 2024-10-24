'''
Servidor que encapsula quadros de video armazenado dentro de pacotes RTP

Baixa resolução: 240p ou 360p, para que o tamanho de cada quadro de vídeo seja pequeno.
Baixa taxa de quadros (frame rate): 15 ou 24 FPS, o que reduz a quantidade de quadros processados por segundo.
Curta duração: 10 a 30 segundos, para que o teste não leve muito tempo.

'''
import socket

# Configurações do servidor para teste local
HOST = '127.0.0.1'  # Escuta apenas no localhost
PORT = 5004         # Porta que o servidor irá escutar

def start_server():
    # Cria um socket UDP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((HOST, PORT))
    print(f"Servidor escutando em {HOST}:{PORT}")

    while True:
        # Recebe dados do cliente
        data, addr = server_socket.recvfrom(2048)  # Tamanho máximo do datagrama
        print(f"Recebido {len(data)} bytes de {addr}")

        # Processa o pacote recebido (exemplo: imprime os bytes)
        print(f"Dados: {data}")

if __name__ == "__main__":
    start_server()
