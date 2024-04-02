import socket
import _thread

HOST = 'localhost'
PORT = 5000

match = {
    "word": "coisar",
    "player1_id": None,
    "player2_id": None,
    "status": "waiting",
    "vez": 1
}

def verificarPalavra(con, cliente, choosen_Word, msg):
    if(msg == "get_size"):
        con.sendall(bytes(str(len(choosen_Word)).encode()))
    elif(msg == "status"):
        con.sendall(bytes(str(match["status"]).encode()))
    else:
        if((match["player1_id"] == cliente[1] and match["vez"] == 1) or
                ((match["player2_id"] == cliente[1] and match["vez"] == 2))):
            print('Mensagem recebida!')
            word = msg
            print(f"word:{word}")

            if (len(word) == len(choosen_Word)):  # verificando se possui mesmo tamanho
                # cria o vetor no tamanho da palavra
                vetor = []
                for i in range(len(choosen_Word)):
                    vetor.append(0)

                for i in range(len(choosen_Word)):  # verificando se as posições batem
                    if word[i] == choosen_Word[i]:
                        vetor[i] = 1
                        # print('verde')
                    elif word[i] in choosen_Word:
                        vetor[i] = 2
                        # print('laranja')
                print('fim da verificacao')

            else:
                print('Palavras de tamanhos diferentes!')

            print(f"bytes(vetor):{bytes(vetor)}")

            if not checkIfWin(vetor):
                match["vez"] = 1 if match["vez"] == 2 else 2
                match["status"] = "vez do 1" if match["vez"] == 1 else "vez do 2"
            else:
                if checkIfWin(vetor) and match["vez"] == 1:
                    match["status"] = "1 ganhou"
                elif checkIfWin(vetor) and match["vez"] == 2:
                    match["status"] = "2 gahnou"

            con.sendall(bytes(vetor))
            vetor.clear()
        else:
            con.sendall(bytes('3'.encode()))

def checkIfWin(vetor):
    for i in vetor:
        if i != 1:
            return 0
    return 1

def conectado(con, cliente):  # Função chamada quando uma nova thread for iniciada
    if(match["player1_id"] == None):
        match["player1_id"] = cliente[1]
        con.sendall(bytes('1'.encode()))
        print("player 1 entrou...")
    elif(match["player2_id"] == None):
        match["player2_id"] = cliente[1]
        match["status"] = "vez do 1"
        con.sendall(bytes('2'.encode()))
        print("player 2 entrou...")
    else:
        con.sendall(bytes('-1'.encode()))

    while True:
        # Recebendo as mensagens através da conexão
        msg = con.recv(1024)
        if not msg:
            if(match["vez"] == 1 and cliente == match["player1_id"]):
                con.sendall(bytes('vez do 1'.encode()))
            if (match["vez"] == 2 and cliente == match["player2_id"]):
                con.sendall(bytes('vez do 2'.encode()))
            break

        print('\nCliente..:', cliente)
        print('Mensagem.:', msg)
        verificarPalavra(con, cliente, match["word"], msg.decode())

    print('\nFinalizando conexao do cliente', cliente)
    con.close()
    _thread.exit()


tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
orig = (HOST, PORT)

tcp.bind(orig)  # Colocando um endereço IP e uma porta no Socket
tcp.listen(1)  # Colocando o Socket em modo passivo

print('\nServidor TCP concorrente iniciado no IP', HOST, 'na porta', PORT)

while True:
    con, cliente = tcp.accept()  # Aceitando uma nova conexão

    print('\nNova thread iniciada para essa conexão')

    _thread.start_new_thread(conectado, tuple([con, cliente]))  # Abrindo uma thread para a conexão

# Fechando a conexão com o Socket
tcp.close()