import socket
import threading
import json

RENDEZVOUS = ('192.168.1.100', 50000)

class udp:
    
    def __init__(self):
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.ip , self.dport ="0",0
        self.pareado =False
        self.last_msg=""    
    
    def conectar(self): 
        # connect to rendezvous
        print('connecting to rendezvous server...\n\n')

        #escutar numa porta alta disponicel
        self.sock.bind(('0.0.0.0', 0))
        self.sock.sendto(b'0', RENDEZVOUS)
        print("...Listening server in: ",self.sock.getsockname())

        #esperar receber o endereço e socket do peer
        while True:
            data = self.sock.recv(1024).decode()

            if data.strip() == 'ready':
                print('checked in with server, waiting')
                break

        #recebe as informações, necessita tratar caso nao receba, pedindo reenvio       
        data = self.sock.recv(1024).decode()
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()    
        self.ip, sport, self.dport = data.split(' ')
        sport = int(sport)
        self.dport = int(self.dport)

        print('\ngot peer')
        print('  ip:          {}'.format(self.ip))
        print('  source port: {}'.format(sport))
        print('  dest port:   {}\n'.format(self.dport))

        # punch hole
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('0.0.0.0', self.dport))
        self.sock.sendto(b'0', (self.ip, sport))

        print(f'listening in {self.dport} now, ready to exchange messages with\n{self.ip}:{self.dport}')
        self.start_listen()
        self.pareado = True

    def listen(self):

        #sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #"""sock.bind(('0.0.0.0', sport))"""
        
        while True:
            
            try:
                if self.pareado:
                    header = int(self.sock.recv(10).decode())
                    data = self.sock.recv(header)
                    self.last_msg = data.decode()
                    #print('\rpeer: {}\n> '.format(self.last_msg), end='')
            except:
                print("nothing")

            
    def start_listen(self):
        listener = threading.Thread(target=self.listen, daemon=True);
        listener.start()


    def send(self,msg):
        
        header=str(len(msg))
        while len(header)<10: header+=" "
        self.sock.sendto(header.encode(), (self.ip, int(self.dport)))         
        self.sock.sendto(msg.encode(), (self.ip, int(self.dport)))

#exemplo de uso
"""conectar= udp()
conectar.conectar()
dict ={
    'a':'letra a',
    'b':1
}
jason_obt=json.dumps(dict, indent=4)
print("ta ai\n",jason_obt)
conectar.send(jason_obt)
while True:
    conectar.send(input(">"))"""
    




