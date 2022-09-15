import socket

known_port = 50001

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 50000))#servidor escutando nessa
print(f">>>Servidor Iniciado\n\t{sock}\n\n--------------------------------------\n")

while True:
    clients = []

    while True:
        try:
            data, address = sock.recvfrom(128)
            repeatido=False

            """for c in clients:
                if address == c:
                    repeatido = True"""
                    
            if len(clients)==0 or not repeatido:
                print('connection from: {}'.format(address))
                clients.append(address)

                sock.sendto(b'ready', address)

            if len(clients) == 2:
                print('got 2 clients, sending details to each')
                break
        except:pass

    c2 = clients.pop()
    c2_addr, c2_port = c2
    print("C2:",c2)
    c1 = clients.pop()
    c1_addr, c1_port = c1
    print("C1:",c1)
    
                                         #sorcer_port,des_port
    sock.sendto('{} {} {}'.format(c2_addr, c2_port,known_port ).encode(), c1)
    sock.sendto('{} {} {}'.format(c1_addr, c1_port,known_port ).encode(), c2)