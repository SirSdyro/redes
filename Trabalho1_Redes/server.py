import socket
import threading
import os

class User:

    def __init__(self, ipv4, sock, nome = "", email = "Undefined", local = "Undefined",canal = "main"):
        self.ipv4 = ipv4
        self.sock = sock
        self.nome = nome
        self.email = email
        self.local = local
        self.grupos = {}
        self.convites = {}
        self.pedidos = {}
        self.canal = canal

    def setNome(self,nome):
        self.nome = nome

    def setEmail(self,email):
        self.email = email

    def setLoc(self,local):
        self.local = local

    def addGrupo(self,grupo):
        self.grupos.append(grupo)

    def getDados(self):
        canal = self.canal
        if canal == "main":
            return str(f"Nome = {self.nome}\nEmail = {self.email}\nLocal = {self.local}\nCanal = {self.canal}")
        else: 
            return str(f"Nome = {self.nome}\nEmail = {self.email}\nLocal = {self.local}\nCanal = {self.canal.nome}")
    
    def setCanal(self,canal):
        self.canal = canal
    
    def __repr__(self) -> str:
        return f"[{self.nome}/{self.email}/{self.local}]"

class Grupo:
    def __init__(self,adm,nome):
        self.adm = adm
        self.membros = [adm]
        self.nome = nome
        self.files = []

    def getMembros(self):
        j = 0
        for i in self.membros:
            j += 1
            if j == len(self.membros):
                print(i.nome)
            else:
                print(i.nome,end = ' ')

    def entrar(self,user):
        self.membros.append(user)

    def sair(self,user):
        self.membros.remove(user)   
    
def separador(string,tam):
    return [string[:tam],string[tam+1:]]

def listar(lista):
    aux = []
    for i in lista:
        aux.append(i)
    return str(aux)

#############################################################
#############################################################
#############################################################

HEADER = 1024
PORT = 5900
SERVER = socket.gethostbyname(socket.gethostname())
END = (SERVER,PORT)
FORMAT = 'utf-8'
INTRO1 = "/comandos - comandos possíveis no canal atual\n/dados - dados do perfil\n/grupos - grupos que o usuário participa\n/convites - convites recebidos\n/pedidos - pedidos recebidos\n/aceitarConvite <nomedogrupo> - aceita o convite para tal grupo\n/recusarConvite <nomedogrupo> - recusa o convite\n/aceitarPedido <nomeusuario> - aceita o pedido de tal usuario para entrar em determinado grupo\n/recusarPedido <nomeusuario> - recusa o pedido\n/entrar <nomedogrupo> - envia pedido ao adm do grupo para entrar\n/canal <nomedogrupo> - entrar no chat do tal grupo\n/criargrupo <nome> - criar grupo\n"
INTRO2 = "/comandos - comandos possíveis no canal atual\n/dados - dados do perfil\n/membros - mostra membros do grupo\n/grupos - grupos que o usuário participa\n/convites - convites recebidos\n/pedidos - pedidos recebidos\n/arquivos - mostra os arquivos enviados por outros membros do grupo\n/abrir <nomedoarquivo> - Transfere o arquivo selecionado\n/imagem <arquivo> <nomedoarquivo> - envia uma imagem com o determinado nome\n/audio <arquivo> <nomedoarquivo> - envia um aúdio com o determinado nome\n/aceitarConvite <nomedogrupo> - aceita o convite para tal grupo\n/recusarConvite <nomedogrupo> - recusa o convite\n/aceitarPedido <nomeusuario> - aceita o pedido de tal usuario para entrar em determinado grupo\n/recusarPedido <nomeusuario> - recusa o pedido\n/entrar <nomedogrupo> - envia pedido ao adm do grupo para entrar\n/canal <nomedogrupo> - entrar no chat do tal grupo\n/convidar <nomedousuario> - convida o determinado usuário para o grupo\n/sair - retorna para o canal principal\n"

users = []
grupos = {}


class Server(object):
    def __init__(self, hostname, port):
        self.clients = {}

        # create server socket
        self.tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # start server
        self.tcp_server.bind((hostname, port))
        self.tcp_server.listen()

        print("[INFO] APLICAÇÃO CHAT EM GRUPO - VER. 3")
        print("[INFO] Server running on {}:{}".format(hostname, port))

        while True:
            connection, address = self.tcp_server.accept()
            data = connection.recv(1024).decode()
            parts = data.split('\n')
            nickname = parts[0] + f"_{address[1]}"
            email = parts[1]
            local = parts[2]
            perfil = User(address[0], address[1], nickname, email, local)
            users.append(nickname)
            self.clients[perfil] = connection

            # start a thread for the client
            threading.Thread(target=self.receive_message, args=(connection, perfil), daemon=True).start()

            print("[INFO] Connection from {}:{} AKA {}".format(address[0], address[1], nickname))
            


    def receive_message(self, connection, perfil):
        print("[INFO] Waiting for messages")
        aux = perfil
        usuarios = users
        while True:
            try:
                while aux.canal == "main":
                    msg = connection.recv(1024)
                    if msg:
                        line = msg.decode()
                        if line == "/comandos":
                            self.send2client(INTRO1,perfil)

                        elif line == "/dados":
                            self.send2client(aux.getDados(),perfil)

                        elif line == "/refresh":
                            self.userList(str(users),perfil)
                            self.groupRefresh(listar(grupos.keys()),perfil)

                        elif line == "/grupos":
                            self.send2client(str(aux.grupos.keys()),perfil)

                        elif line == "/convites":
                            self.send2client(str(aux.convites.keys()),perfil)

                        elif line == "/pedidos":
                            self.send2client(str(aux.pedidos.keys()),perfil)

                        elif separador(line,len("/aceitarConvite"))[0] == "/aceitarConvite":
                            nomeGrupo = separador(line,len("/aceitarConvite"))[1].strip(" ")
                            if nomeGrupo not in aux.convites:
                                self.send2client(f"[FALHA] Convite do grupo {nomeGrupo} não existente",perfil)
                            else:
                                aux.convites[nomeGrupo][1].grupos[aux.convites[nomeGrupo][0].nome] = aux.convites[nomeGrupo][0]
                                self.send2client(f"Convite para {aux.convites[nomeGrupo][1].nome} para o grupo {nomeGrupo} aceito",aux.convites[nomeGrupo][2])
                                aux.convites[nomeGrupo][0].membros.append(aux.convites[nomeGrupo][1])
                                aux.convites.pop(nomeGrupo)

                        elif separador(line,len("/recusarConvite"))[0] == "/recusarConvite":
                            nomeGrupo = separador(line,len("/recusarConvite"))[1].strip(" ")
                            if nomeGrupo not in aux.convites:
                                self.send2client(f"[FALHA] Convite do grupo {nomeGrupo} não existente",perfil)
                            else:
                                self.send2client(f"Convite para {aux.convites[nomeGrupo][0].nome} para o grupo {nomeGrupo} recusado",aux.convites[nomeGrupo][1])
                                aux.convites.pop(nomeGrupo)

                        elif separador(line,len("/aceitarPedido"))[0] == "/aceitarPedido":
                            nomeUser = separador(line,len("/aceitarPedido"))[1]
                            if nomeUser not in aux.pedidos:
                                self.send2client(f"[FALHA] Pedido de {nomeUser} não existente",perfil)
                            else:
                                aux.pedidos[nomeUser][1].grupos[aux.pedidos[nomeUser][0].nome] = aux.pedidos[nomeUser][0]
                                aux.pedidos[nomeUser][0].membros.append(aux.pedidos[nomeUser][1])
                                self.send2client(f"Pedido para o grupo {aux.pedidos[nomeUser][0].nome} de {nomeUser} aceito",aux.pedidos[nomeUser][1])
                                aux.pedidos.pop(nomeUser)

                        elif separador(line,len("/recusarPedido"))[0] == "/recusarPedido":
                            nomeUser = separador(line,len("/recusarPedido"))[1]
                            if nomeUser not in aux.pedidos:
                                self.send2client(f"[FALHA] Pedido de {nomeUser} não existente",perfil)
                            else:
                                self.send2client(f"Pedido para o grupo {aux.pedidos[nomeUser][0].nome} de {nomeUser} recusado",aux.pedidos[nomeUser][1])
                                aux.pedidos.pop(nomeUser)

                        elif separador(line,len("/entrar"))[0] == "/entrar":
                            nomeGrupo = separador(line,len("/entrar"))[1]
                            if nomeGrupo not in grupos:
                                self.send2client(f"[FALHA] Grupo {nomeGrupo} não existente",perfil)
                            else:
                                pedido = (grupos[nomeGrupo],perfil)
                                adm = grupos[nomeGrupo].adm
                                self.send2client(f"[PEDIDO] Novo pedido para entrar no grupo {nomeGrupo} de {perfil.nome}",adm)
                                adm.pedidos[perfil.nome] = pedido

                        elif separador(line,len("/criargrupo"))[0] == "/criargrupo":
                            nomeGrupo = separador(line,len("/criargrupo"))[1]
                            if nomeGrupo in grupos:
                                self.send2client(f"[FALHA] Nome de grupo já existente",perfil)
                            else:
                                grupo = Grupo(aux,nomeGrupo)
                                aux.grupos[nomeGrupo] = grupo
                                grupos[nomeGrupo] = grupo
                                self.send2client(f"[SUCESSO] Grupo {nomeGrupo} criado",perfil)
                                self.groupList(listar(grupos.keys()))
                        
                        elif separador(line,len("/canal"))[0] == "/canal":
                            nomeGrupo = separador(line,len("/canal"))[1]
                            if nomeGrupo in grupos:
                                if nomeGrupo in aux.grupos:
                                    aux.canal = aux.grupos[nomeGrupo]
                                    self.send2client(f"[ENTRANDO] Entrando no grupo {nomeGrupo}",perfil)
                                    self.channel(nomeGrupo,perfil)
                                else:
                                    self.send2client(f"[FALHA] O usuário não faz parte do grupo {nomeGrupo}",perfil)
                            else:
                                self.send2client(f"[FALHA] O grupo {nomeGrupo} não existe",perfil)

                while aux.canal in grupos.values():
                    grupo = aux.canal
                    msg = connection.recv(1024)
                    if msg:
                        line = msg.decode()
                        if line == "/comandos":
                            self.send2client(INTRO2,perfil)

                        elif line == "/dados":
                            self.send2client(aux.getDados(),perfil)

                        elif line == "/refresh":
                            self.userList(str(users),perfil)
                            self.groupRefresh(listar(grupos.keys()),perfil)

                        elif line == "/membros":
                            self.send2client(str(grupo.membros),perfil)

                        elif line == "/grupos":
                            self.send2client(str(aux.grupos.keys()),perfil)

                        elif line == "/convites":
                            self.send2client(str(aux.convites.keys()),perfil)

                        elif line == "/pedidos":
                            self.send2client(str(aux.pedidos.keys()),perfil)

                        elif line == "/arquivos":
                            self.send2client(str(aux.canal.files),perfil)

                        #elif line == "/abrir":
                            #self.send2client("[AGUARDE] Recebendo arquivo...",perfil)
                            #file = open("goku.png", "rb")
                            #file_size = os.path.getsize("goku.png")
                            #print(str(file_size))
                            #self.clients[perfil].send(str(file_size).encode())
                            #data = file.read()
                            #self.clients[perfil].sendall(data)
                            #file.close()

                        elif line == "<donwloadconluido>":
                            self.send2client("[SUCESSO] Arquivo recebido",perfil)

                        elif separador(line,len("/abrir"))[0] == "/abrir":
                            if separador(line,len("/abrir"))[1].strip(" ") in aux.canal.files:
                                self.send2client("[AGUARDE] Recebendo arquivo...",perfil)
                                file = open(separador(line,len("/abrir"))[1], "rb")
                                file_size = os.path.getsize(separador(line,len("/abrir"))[1])
                                print(str(file_size))
                                self.clients[perfil].send(str(file_size).encode())
                                data = file.read()
                                self.clients[perfil].sendall(data)
                                file.close()
                            else:
                                self.send2client("[FALHA] Arquivo não existente")

                        elif line == "/imagem":
                            data = connection.recv(1024).decode()
                            data = data.split()
                            file_name = data[0]
                            file_size = data[1]
                            print(file_name)
                            print(file_size)
                            file = open(file_name,"wb")
                            file_bytes = b""
                            done = False
                            while not done:
                                data = connection.recv(1024)
                                if file_bytes[-5:] == b"<END>":
                                    done =  True
                                else:
                                    file_bytes += data
                            file.write(file_bytes)
                            file.close()
                            aux.canal.files.append(file_name)
                            self.send2client("[SUCESSO] Imagem recebida",perfil)

                        elif line == "/audio":
                            data = connection.recv(1024).decode()
                            data = data.split()
                            file_name = data[0]
                            file_size = data[1]
                            print(file_name)
                            print(file_size)
                            file = open(file_name,"wb")
                            file_bytes = b""
                            done = False
                            while not done:
                                data = connection.recv(1024)
                                if file_bytes[-5:] == b"<END>":
                                    done =  True
                                else:
                                    file_bytes += data
                            file.write(file_bytes)
                            file.close()
                            aux.canal.files.append(file_name)
                            self.send2client("[SUCESSO] Audio recebido",perfil)

                        elif separador(line,len("/aceitarConvite"))[0] == "/aceitarConvite":
                            nomeGrupo = separador(line,len("/aceitarConvite"))[1].strip(" ")
                            if nomeGrupo not in aux.convites:
                                self.send2client(f"[FALHA] Convite do grupo {nomeGrupo} não existente",perfil)
                            else:
                                aux.convites[nomeGrupo][1].grupos[aux.convites[nomeGrupo][0].nome] = aux.convites[nomeGrupo][0]
                                self.send2client(f"Convite para {aux.convites[nomeGrupo][1].nome} para o grupo {nomeGrupo} aceito",aux.convites[nomeGrupo][2])
                                aux.convites[nomeGrupo][0].membros.append(aux.convites[nomeGrupo][1])
                                aux.convites.pop(nomeGrupo)

                        elif separador(line,len("/recusarConvite"))[0] == "/recusarConvite":
                            nomeGrupo = separador(line,len("/recusarConvite"))[1].strip(" ")
                            if nomeGrupo not in aux.convites:
                                self.send2client(f"[FALHA] Convite do grupo {nomeGrupo} não existente",perfil)
                            else:
                                self.send2client(f"Convite para {aux.convites[nomeGrupo][0].nome} para o grupo {nomeGrupo} recusado",aux.convites[nomeGrupo][1])
                                aux.convites.pop(nomeGrupo)

                        elif separador(line,len("/aceitarPedido"))[0] == "/aceitarPedido":
                            nomeUser = separador(line,len("/aceitarPedido"))[1]
                            if nomeUser not in aux.pedidos:
                                self.send2client(f"[FALHA] Pedido de {nomeUser} não existente",perfil)
                            else:
                                aux.pedidos[nomeUser][1].grupos[aux.pedidos[nomeUser][0].nome] = aux.pedidos[nomeUser][0]
                                aux.pedidos[nomeUser][0].membros.append(aux.pedidos[nomeUser][1])
                                self.send2client(f"Pedido para o grupo {aux.pedidos[nomeUser][0].nome} de {nomeUser} aceito",aux.pedidos[nomeUser][1])
                                aux.pedidos.pop(nomeUser)

                        elif separador(line,len("/recusarPedido"))[0] == "/recusarPedido":
                            nomeUser = separador(line,len("/recusarPedido"))[1]
                            if nomeUser not in aux.pedidos:
                                self.send2client(f"[FALHA] Pedido de {nomeUser} não existente",perfil)
                            else:
                                self.send2client(f"Pedido para o grupo {aux.pedidos[nomeUser][0].nome} de {nomeUser} recusado",aux.pedidos[nomeUser][1])
                                aux.pedidos.pop(nomeUser)

                        elif separador(line,len("/entrar"))[0] == "/entrar":
                            nomeGrupo = separador(line,len("/entrar"))[1]
                            if nomeGrupo not in grupos:
                                self.send2client(f"[FALHA] Grupo {nomeGrupo} não existente",perfil)
                            else:
                                pedido = (grupos[nomeGrupo],perfil)
                                adm = grupos[nomeGrupo].adm
                                self.send2client(f"[PEDIDO] Novo pedido para entrar no grupo {nomeGrupo} de {perfil.nome}",adm)
                                adm.pedidos[perfil.nome] = pedido

                        elif separador(line,len("/canal"))[0] == "/canal":
                            nomeGrupo = separador(line,len("/canal"))[1]
                            if nomeGrupo in grupos:
                                if nomeGrupo in aux.grupos:
                                    aux.canal = aux.grupos[nomeGrupo]
                                    self.send2client(f"[ENTRANDO] Entrando no grupo {nomeGrupo}",perfil)
                                    self.channel(nomeGrupo,perfil)
                                else:
                                    self.send2client(f"[FALHA] O usuário não faz parte do grupo {nomeGrupo}",perfil)
                            else:
                                self.send2client(f"[FALHA] O grupo {nomeGrupo} não existe",perfil)

                        elif separador(line,len("/convidar"))[0] == "/convidar":
                            usuario = separador(line,len("/convidar"))[1].strip(" ")
                            if usuario in users:
                                for i in self.clients:
                                    if i.nome == usuario:
                                        invite = [grupo,i,perfil]
                                        i.convites[grupo.nome] = invite
                                        self.send2client(f"[CONVITE] Novo convite para o grupo {grupo.nome}",i)
                                        self.send2client(f"[SUCESSO] Convite enviado",perfil)
                            else:
                                self.send2client(f"[FALHA] Usuário não existente",perfil)
                                
                        elif line == "/sair":
                            aux.canal = "main"
                            self.send2client(f"[SAINDO] Saindo do grupo {grupo.nome}",perfil)
                            self.channel("Tela Principal",perfil)
                        
                        else:
                            self.send_message(msg, perfil, aux.canal)
                            print(perfil.nome + ": " + line)

            except:
                connection.close()

                #remove user from users list
                users.remove(perfil.nome)
                del(self.clients[perfil])
                for i in perfil.grupos:
                    perfil.grupos[i].membros.remove(perfil)

                break

        print(perfil.nome, " disconnected")


    def send_message(self, message, sender, grupo):
        if len(grupo.membros) > 0:
            for nickname in grupo.membros:
                if nickname != sender and nickname.canal == grupo:
                    msg = sender.nome + ": " + message.decode()
                    self.clients[nickname].send(msg.encode())

    def send2client(self,message,sender):
        msg = "#cl" + message
        self.clients[sender].send(msg.encode())

    def userList(self,message,sender):
        msg = "#ul" + message
        self.clients[sender].send(msg.encode())

    def groupRefresh(self,message,sender):
        msg = "#gl" + message
        self.clients[sender].send(msg.encode())

    def groupList(self,message):
        msg = "#gl" + message
        for nickname in self.clients:
            self.clients[nickname].send(msg.encode())

    def channel(self,message,sender):
        msg = "#ch" + message
        self.clients[sender].send(msg.encode())

if __name__ == "__main__":
    port = 5900
    hostname = "192.168.15.10"

    chat_server = Server(hostname, port)