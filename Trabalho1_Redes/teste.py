def send2client(self, message, sender):
        msg = "c"+message.decode()
        self.clients[sender].send(msg.encode())

def userList(self,message,sender):
        msg = "u"+message.decode()
        self.clients[sender].send(msg.encode())

def groupList(self,message,sender):
        msg = "g"+message.decode()
        self.clients[sender].send(msg.encode())

def show_message(self, message):
        if message[0] == "c":
            self.chat_ui.serverMsgBrowser.append(message[1:])
        elif message[0] == "u":
            self.chat_ui.userBrowser.append(message[1:])
        else:
            self.chat_ui.messageBrowser.append(message)

while True:
            connection, address = self.tcp_server.accept()
            data = connection.recv(1024).decode()
            parts = data.split('\n')
            nickname = parts[0]
            email = parts[1]
            local = parts[2]
            perfil = User(address[0], address[1], nickname, email, local)
            self.clients[perfil] = connection

            # start a thread for the client
            threading.Thread(target=self.receive_message, args=(connection, perfil), daemon=True).start()

            print("[INFO] Connection from {}:{} AKA {}".format(address[0], address[1], nickname))

def handler(client,end):
    print(f"[NEW CONNECTION] {end} connected")
    aux = User(client,end,f'User {end[1]}')
    users.append(aux)

    if aux.canal == "main":
        while aux.canal == "main":
            msg_length = client.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = client.recv(msg_length).decode(FORMAT)
                
                if msg == "/end":
                    print(f"[{aux.nome} disconnected]")
                    client.close()
                    
                elif msg == "/comandos":
                    client.send(INTRO.encode(FORMAT))

                elif msg == "/dados":
                    client.send(aux.getDados().encode(FORMAT))

                elif msg == "/users":
                    client.send(str(users).encode(FORMAT))

                elif msg == "/grupos":
                    client.send(str(grupos).encode(FORMAT))

                elif separador(msg,len("/setnome"))[0] == "/setnome":
                    aux.setNome(separador(msg,len("/setnome"))[1])
                    client.send("Novo nome definido".encode(FORMAT))

                elif separador(msg,len("/setemail"))[0] == "/setemail":
                    aux.setEmail(separador(msg,len("/setemail"))[1])
                    client.send("Novo email definido".encode(FORMAT))

                elif separador(msg,len("/setlocal"))[0] == "/setlocal":
                    aux.setLoc(separador(msg,len("/setlocal"))[1])
                    client.send("Novo local definido".encode(FORMAT))

                elif separador(msg,len("/criarGrupo"))[0] == "/criargrupo":
                    nomeGrupo = separador(msg,len("/criargrupo"))[1]
                    if nomeGrupo in listar(grupos):
                        client.send(f"Falha: Nome de grupo já existente".encode(FORMAT))
                    else:
                        grupo = Grupo(aux,nomeGrupo)
                        aux.addGrupo(grupo)
                        grupos.append(grupo)
                        client.send(f"Sucesso: Grupo {grupo.nome} criado".encode(FORMAT))
                
                elif separador(msg,len("/entrar"))[0] == "/entrar":
                    nomeGrupo = separador(msg,len("/entrar"))[1]
                    if nomeGrupo in listar(grupos):
                        if nomeGrupo in listar(aux.grupos):
                            aux.canal = grupos[listar(grupos).index(nomeGrupo)]
                            client.send(f"[ENTRANDO] Entrando no grupo {nomeGrupo}".encode(FORMAT))
                            canalHandler(client,end,aux,grupos,)
                        else:
                            client.send(f"Falha: O usuário não faz parte do grupo {nomeGrupo}".encode(FORMAT))
                    else:
                        client.send(f"Falha: O grupo {nomeGrupo} não existe".encode(FORMAT))
                elif msg == "/aderir Teste":
                    aux.addGrupo(grupos[listar(grupos).index("Teste")])
                    client.send(f"Entrou no grupo Teste".encode(FORMAT))
                else:
                    print(f"[{aux.nome}]: {msg}")
                    client.send("Msg received".encode(FORMAT))

elif separador(line,len("/setnome"))[0] == "/setnome":
                            aux.setNome(separador(line,len("/setnome"))[1])
                            self.send2client("Novo nome definido",perfil)

                        elif separador(line,len("/setemail"))[0] == "/setemail":
                            aux.setEmail(separador(line,len("/setemail"))[1])
                            self.send2client("Novo email definido",perfil)

                        elif separador(line,len("/setlocal"))[0] == "/setlocal":
                            aux.setLoc(separador(line,len("/setlocal"))[1])
                            self.send2client("Novo local definido",perfil)